"""
PyUI development server — aiohttp-based.

Serves compiled HTML pages, handles event POSTs from the browser,
hot-reloads on file changes via WebSocket, and provides a theme-swap API.

Usage (internal — called by the CLI ``run`` command)::

    from pyui.server.dev_server import run_dev_server
    run_dev_server(MyApp, host="localhost", port=8000)
"""

from __future__ import annotations

import asyncio
import contextlib
import importlib
import importlib.util
import inspect
import json
import sys
import threading
import webbrowser
from pathlib import Path
from typing import TYPE_CHECKING, Any

from aiohttp import web

from pyui.compiler.ir import build_ir_tree, get_handler
from pyui.renderers.web.generator import WebGenerator
from pyui.utils.logging import get_logger

if TYPE_CHECKING:
    from pyui.app import App

log = get_logger(__name__)


def _reimport_app(module_path: str, original_class: type[App]) -> type[App]:
    """
    Re-import the user's module from disk and return the refreshed App subclass.

    This is the key to hot reload — we force Python to re-execute the module
    file so any edits the user made are picked up.
    """
    from pyui.app import App as AppBase

    path = Path(module_path).resolve()
    module_name = f"_pyui_hot_{path.stem}"

    # Remove the old cached module so importlib re-executes the file
    sys.modules.pop(module_name, None)

    spec = importlib.util.spec_from_file_location(module_name, str(path))
    if spec is None or spec.loader is None:
        return original_class

    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)  # type: ignore[union-attr]
    except Exception as exc:
        raise RuntimeError(str(exc)) from exc

    # Find the App subclass in the freshly-loaded module
    for _name, obj in inspect.getmembers(module, inspect.isclass):
        if issubclass(obj, AppBase) and obj is not AppBase:
            return obj  # type: ignore[return-value]

    return original_class


class PyUIDevServer:
    """
    The PyUI development server.

    Parameters
    ----------
    app_class : type[App]
        The user's App subclass.
    host : str
    port : int
    open_browser : bool
        Whether to open the default browser on startup.
    watch_file : str | None
        Path to the app file to watch for hot-reload.
    """

    def __init__(
        self,
        app_class: type[App],
        host: str = "localhost",
        port: int = 8000,
        open_browser: bool = True,
        watch_file: str | None = None,
    ) -> None:
        self.app_class = app_class
        self.host = host
        self.port = port
        self.open_browser = open_browser
        self.watch_file = watch_file

        # Compiled state — rebuilt on hot-reload
        self._ir_tree = build_ir_tree(app_class)
        self._generator = WebGenerator(self._ir_tree)
        self._route_map = {p.route: p for p in self._ir_tree.pages}

        # Active WebSocket connections — populated after loop starts
        self._ws_clients: set[web.WebSocketResponse] = set()
        # Lock created lazily inside the running loop to avoid "no running loop" errors
        self._ws_lock: asyncio.Lock | None = None

        # asyncio event loop reference (set when server starts)
        self._loop: asyncio.AbstractEventLoop | None = None

    def _get_lock(self) -> asyncio.Lock:
        if self._ws_lock is None:
            self._ws_lock = asyncio.Lock()
        return self._ws_lock

    # ── Hot reload ────────────────────────────────────────────────────────────

    def _on_file_change(self, changed_path: str) -> None:
        """Called by the file watcher thread when a .py file changes."""
        log.debug("Hot reload triggered", path=changed_path)

        try:
            # Re-import the module from disk to pick up the user's edits
            if self.watch_file:
                new_class = _reimport_app(self.watch_file, self.app_class)
                self.app_class = new_class

            from pyui.compiler.ir import clear_registry
            clear_registry()
            self._ir_tree = build_ir_tree(self.app_class)
            self._generator = WebGenerator(self._ir_tree)
            self._route_map = {p.route: p for p in self._ir_tree.pages}
        except Exception as exc:
            log.error("Hot reload compile error", error=str(exc))
            if self._loop and self._loop.is_running():
                asyncio.run_coroutine_threadsafe(
                    self._broadcast({"type": "error", "message": str(exc)}),
                    self._loop,
                )
            return

        if self._loop and self._loop.is_running():
            asyncio.run_coroutine_threadsafe(
                self._broadcast({"type": "reload"}),
                self._loop,
            )

    async def _broadcast(self, message: dict[str, Any]) -> None:
        """Send *message* to all connected WebSocket clients."""
        lock = self._get_lock()
        async with lock:
            dead: set[web.WebSocketResponse] = set()
            for ws in self._ws_clients:
                try:
                    await ws.send_json(message)
                except Exception:
                    dead.add(ws)
            self._ws_clients -= dead

    # ── Request handlers ──────────────────────────────────────────────────────

    async def _handle_ws(self, request: web.Request) -> web.WebSocketResponse:
        """WebSocket endpoint — used for hot-reload broadcasts."""
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        await ws.send_json({"type": "connected", "version": "0.1.0"})
        log.debug("WebSocket client connected", remote=str(request.remote))

        lock = self._get_lock()
        async with lock:
            self._ws_clients.add(ws)

        try:
            async for _msg in ws:
                pass
        finally:
            async with lock:
                self._ws_clients.discard(ws)

        return ws

    async def _handle_theme(self, request: web.Request) -> web.Response:
        """POST /pyui-api/theme/{name} — hot-swap the app theme."""
        theme_name = request.match_info["name"]
        from pyui.exceptions import ThemeError
        from pyui.theme.engine import build_theme, tokens_to_css_vars

        try:
            tokens = build_theme(theme_name)
        except ThemeError as exc:
            return web.Response(
                status=400,
                text=json.dumps({"error": str(exc)}),
                content_type="application/json",
            )

        self.app_class.theme = theme_name
        css = tokens_to_css_vars(tokens)
        return web.Response(
            text=json.dumps({"theme": theme_name, "css": css}),
            content_type="application/json",
        )

    async def _handle_page(self, request: web.Request) -> web.Response:
        """Serve the HTML page for the requested route."""
        path = request.path
        ir_page = self._route_map.get(path) or self._route_map.get(
            "/" if path == "" else path.rstrip("/")
        )
        if ir_page is None:
            ir_page = self._route_map.get("/")
        if ir_page is None:
            return web.Response(
                text=self._not_found_html(path),
                content_type="text/html",
                status=404,
            )

        # Rebuild IR to pick up reactive-var changes since last request
        self._ir_tree = build_ir_tree(self.app_class)
        self._generator = WebGenerator(self._ir_tree)
        self._route_map = {p.route: p for p in self._ir_tree.pages}
        ir_page = self._route_map.get(path) or self._route_map.get("/")

        html = self._generator.render_ir_page(ir_page)  # type: ignore[arg-type]
        return web.Response(text=html, content_type="text/html")

    async def _handle_event(self, request: web.Request) -> web.Response:
        """POST /pyui-api/event/{handler_id} — invoke a Python event handler."""
        handler_id = request.match_info["handler_id"]
        if handler_id == "update_state":
            try:
                data = await request.json()
                updates = data.get("data", {})
                from pyui.state.reactive import ReactiveVar
                for attr_name, new_val in updates.items():
                    for name, value in inspect.getmembers(self.app_class):
                        if name == attr_name and isinstance(value, ReactiveVar):
                            value.set(new_val)
            except Exception as exc:
                log.error("State update failed", error=str(exc))
                return web.Response(
                    status=400,
                    text=json.dumps({"error": str(exc)}),
                    content_type="application/json",
                )
        else:
            handler = get_handler(handler_id)
            if handler is None:
                return web.Response(
                    status=404,
                    text=json.dumps({"error": f"Unknown handler: {handler_id}"}),
                    content_type="application/json",
                )
            with contextlib.suppress(Exception):
                await request.json() if request.body_exists else {}
            try:
                result = handler()
                if asyncio.iscoroutine(result):
                    await result
            except Exception as exc:
                log.error("Event handler raised", handler_id=handler_id, error=str(exc))
                return web.Response(
                    status=500,
                    text=json.dumps({"error": str(exc)}),
                    content_type="application/json",
                )

        from pyui.state.reactive import ReactiveVar
        state: dict[str, Any] = {}
        for attr_name, value in inspect.getmembers(self.app_class):
            if isinstance(value, ReactiveVar):
                state[attr_name] = value.get()

        self._ir_tree = build_ir_tree(self.app_class)
        self._generator = WebGenerator(self._ir_tree)

        node_updates: dict[str, dict[str, Any]] = {}
        for page in self._ir_tree.pages:
            self._collect_node_updates(page.children, node_updates)

        return web.Response(
            text=json.dumps({"state": state, "nodes": node_updates, "reload": False}),
            content_type="application/json",
        )

    async def _handle_devtools_state(self, request: web.Request) -> web.Response:
        """GET /pyui-api/devtools/state — return current reactive state snapshot."""
        from pyui.state.reactive import ReactiveVar
        state: dict[str, Any] = {}
        for attr_name, value in inspect.getmembers(self.app_class):
            if isinstance(value, ReactiveVar):
                state[attr_name] = value.get()
        return web.Response(
            text=json.dumps({"state": state, "app": self.app_class.__name__}),
            content_type="application/json",
        )

    def _collect_node_updates(self, nodes: list[Any], updates: dict[str, dict[str, Any]]) -> None:
        def _collect(nodes: list[Any]) -> None:
            for n in nodes:
                if n.reactive_props:
                    updates[n.node_id] = {k: n.props.get(k) for k in n.reactive_props}
                if n.children:
                    _collect(n.children)
        _collect(nodes)

    # ── Static helpers ────────────────────────────────────────────────────────

    @staticmethod
    def _not_found_html(path: str) -> str:
        import html as h
        return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>404 — PyUI</title>
<script src="https://cdn.tailwindcss.com"></script></head>
<body class="min-h-screen flex items-center justify-center bg-gray-50">
  <div class="text-center">
    <h1 class="text-6xl font-bold text-violet-600">404</h1>
    <p class="mt-4 text-xl text-gray-600">No page found at
      <code class="bg-gray-100 px-2 py-1 rounded">{h.escape(path)}</code>
    </p>
    <a href="/" class="mt-6 inline-block text-violet-600 hover:underline">Back home</a>
  </div>
</body></html>"""

    # ── Run ───────────────────────────────────────────────────────────────────

    def build_aiohttp_app(self) -> web.Application:
        """Build and return the configured aiohttp Application."""
        aio_app = web.Application()
        aio_app.router.add_post("/pyui-api/event/{handler_id}", self._handle_event)
        aio_app.router.add_post("/pyui-api/theme/{name}", self._handle_theme)
        aio_app.router.add_get("/pyui-api/devtools/state", self._handle_devtools_state)
        aio_app.router.add_get("/pyui-api/ws", self._handle_ws)
        aio_app.router.add_get("/{path:.*}", self._handle_page)
        return aio_app

    def start(self) -> None:
        """Start the dev server (blocking)."""
        aio_app = self.build_aiohttp_app()
        url = f"http://{self.host}:{self.port}"

        from rich import box
        from rich.console import Console
        from rich.panel import Panel
        console = Console()

        hot_reload_status = (
            f"  Hot reload : [green]ON[/green] [dim](watching {Path(self.watch_file).name})[/dim]"
            if self.watch_file
            else "  Hot reload : [dim]OFF[/dim]"
        )

        console.print(
            Panel.fit(
                f"[bold cyan]PyUI Dev Server[/bold cyan]\n\n"
                f"  URL     : [link={url}][cyan]{url}[/cyan][/link]\n"
                f"  App     : [dim]{self.app_class.__name__}[/dim]\n"
                f"  Pages   : [dim]{len(self._ir_tree.pages)} routes[/dim]\n"
                f"{hot_reload_status}\n\n"
                f"[dim]Press Ctrl+C to stop.[/dim]",
                box=box.ASCII,
                border_style="cyan",
            )
        )

        if self.open_browser:
            def _open() -> None:
                import time
                time.sleep(0.8)
                webbrowser.open(url)
            threading.Thread(target=_open, daemon=True).start()

        watcher = None
        if self.watch_file:
            from pyui.hotreload.watcher import FileWatcher
            watch_dir = str(Path(self.watch_file).parent)
            watcher = FileWatcher(watch_dir, on_change=self._on_file_change)
            watcher.start()

        try:
            async def _run() -> None:
                self._loop = asyncio.get_running_loop()
                # Create the lock inside the running loop
                self._ws_lock = asyncio.Lock()
                runner = web.AppRunner(aio_app)
                await runner.setup()
                site = web.TCPSite(runner, self.host, self.port)
                await site.start()
                try:
                    await asyncio.Event().wait()
                finally:
                    await runner.cleanup()

            asyncio.run(_run())
        except KeyboardInterrupt:
            pass
        finally:
            if watcher:
                watcher.stop()


def run_dev_server(
    app_class: type[App],
    host: str = "localhost",
    port: int = 8000,
    open_browser: bool = True,
    watch_file: str | None = None,
) -> None:
    """Convenience function — create a PyUIDevServer and start it."""
    server = PyUIDevServer(
        app_class, host=host, port=port,
        open_browser=open_browser, watch_file=watch_file,
    )
    server.start()
