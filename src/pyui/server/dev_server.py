"""
PyUI development server — aiohttp-based.

Serves compiled HTML pages, handles event POSTs from the browser, and
provides a WebSocket stub for hot-reload (implemented in Phase 6).

Usage (internal — called by the CLI ``run`` command)::

    from pyui.server.dev_server import run_dev_server
    run_dev_server(MyApp, host="localhost", port=8000)
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import webbrowser
from typing import TYPE_CHECKING, Any

from aiohttp import web

from pyui.compiler.ir import build_ir_tree, get_handler
from pyui.renderers.web.generator import WebGenerator
from pyui.utils.logging import get_logger

if TYPE_CHECKING:
    from pyui.app import App

log = get_logger(__name__)


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
    """

    def __init__(
        self,
        app_class: type[App],
        host: str = "localhost",
        port: int = 8000,
        open_browser: bool = True,
    ) -> None:
        self.app_class = app_class
        self.host = host
        self.port = port
        self.open_browser = open_browser

        # Compiled state — rebuilt on hot-reload
        self._ir_tree = build_ir_tree(app_class)
        self._generator = WebGenerator(self._ir_tree)

        # Route → IRPage index for lookups
        self._route_map = {p.route: p for p in self._ir_tree.pages}

    # ── aiohttp request handlers ──────────────────────────────────────────────

    async def _handle_page(self, request: web.Request) -> web.Response:
        """Serve the HTML page for the requested route."""
        path = request.path

        # Normalize: "/" and "" both match the root page
        ir_page = self._route_map.get(path) or self._route_map.get(
            "/" if path == "" else path.rstrip("/")
        )

        if ir_page is None:
            # Try to serve root for any unmatched path (SPA-style fallback)
            ir_page = self._route_map.get("/")

        if ir_page is None:
            return web.Response(
                text=self._not_found_html(path),
                content_type="text/html",
                status=404,
            )

        # Rebuild IR to pick up any reactive-var changes
        self._ir_tree = build_ir_tree(self.app_class)
        self._generator = WebGenerator(self._ir_tree)
        self._route_map = {p.route: p for p in self._ir_tree.pages}
        ir_page = self._route_map.get(path) or self._route_map.get("/")

        html = self._generator.render_ir_page(ir_page)  # type: ignore[arg-type]
        return web.Response(text=html, content_type="text/html")

    async def _handle_event(self, request: web.Request) -> web.Response:
        """
        POST /pyui-api/event/{handler_id}

        Calls the registered Python handler, then returns:
          {"state": {...current reactive state...}, "reload": false}
        """
        handler_id = request.match_info["handler_id"]
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

        # Snapshot updated reactive state
        import inspect

        from pyui.state.reactive import ReactiveVar

        state: dict[str, Any] = {}
        for attr_name, value in inspect.getmembers(self.app_class):
            if isinstance(value, ReactiveVar):
                state[attr_name] = value.get()

        return web.Response(
            text=json.dumps({"state": state, "reload": True}),
            content_type="application/json",
        )

    async def _handle_ws(self, request: web.Request) -> web.WebSocketResponse:
        """WebSocket stub — sends a 'connected' message, then keeps alive."""
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        await ws.send_json({"type": "connected", "version": "0.1.0"})
        log.debug("WebSocket client connected", remote=str(request.remote))
        async for _msg in ws:
            pass  # Hot-reload messages handled in Phase 6
        return ws

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
        console.print(
            Panel.fit(
                f"[bold cyan]PyUI Dev Server[/bold cyan]\n\n"
                f"  URL     : [link={url}][cyan]{url}[/cyan][/link]\n"
                f"  App     : [dim]{self.app_class.__name__}[/dim]\n"
                f"  Pages   : [dim]{len(self._ir_tree.pages)} routes[/dim]\n\n"
                f"[dim]Press Ctrl+C to stop.[/dim]",
                box=box.ASCII,
                border_style="cyan",
            )
        )

        if self.open_browser:
            import threading

            def _open() -> None:
                import time

                time.sleep(0.8)
                webbrowser.open(url)

            threading.Thread(target=_open, daemon=True).start()

        web.run_app(
            aio_app,
            host=self.host,
            port=self.port,
            print=lambda *_: None,  # suppress aiohttp's own startup message
        )


def run_dev_server(
    app_class: type[App],
    host: str = "localhost",
    port: int = 8000,
    open_browser: bool = True,
) -> None:
    """
    Convenience function — create a :class:`PyUIDevServer` and start it.

    Parameters
    ----------
    app_class : type[App]
    host : str
    port : int
    open_browser : bool
    """
    server = PyUIDevServer(app_class, host=host, port=port, open_browser=open_browser)
    server.start()
