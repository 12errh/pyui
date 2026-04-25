"""
PyUI Landing Page — showcase that beautiful UIs can be built with pure Python.

Run with: pyui run landing.py
"""

from pyui import (
    App,
    Avatar,
    Badge,
    Button,
    Container,
    Divider,
    Flex,
    Grid,
    Heading,
    Icon,
    Page,
    Stat,
    Text,
)
from pyui.components.display.rawhtml import RawHTML


# ── Reusable helpers ──────────────────────────────────────────────────────────


def _feature_card(icon: str, title: str, desc: str) -> Flex:
    card = Flex(direction="col", gap=3).className(
        "bg-white rounded-2xl p-6 border border-gray-100 "
        "shadow-[0_1px_3px_rgba(0,0,0,0.06)] "
        "hover:shadow-[0_8px_30px_rgba(0,0,0,0.08)] "
        "hover:-translate-y-0.5 transition-all duration-300"
    )
    with card:
        with Flex(align="center", justify="center").className(
            "w-10 h-10 rounded-xl bg-gray-950 flex-shrink-0"
        ):
            Icon(icon, size=18).className("text-white")
        Heading(title, level=4)
        Text(desc).style("muted").paragraph()
    return card


def _code_block(code: str) -> RawHTML:
    import html as h
    return RawHTML(
        f'<pre class="bg-gray-950 text-gray-100 rounded-2xl p-6 text-sm '
        f'font-mono leading-relaxed overflow-x-auto border border-gray-800">'
        f'<code>{h.escape(code)}</code></pre>'
    )


def _testimonial(quote: str, name: str, role: str, initials: str) -> Flex:
    card = Flex(direction="col", gap=4).className(
        "bg-white rounded-2xl p-6 border border-gray-100 "
        "shadow-[0_1px_3px_rgba(0,0,0,0.06)]"
    )
    with card:
        # Stars
        RawHTML(
            '<div class="flex gap-0.5">'
            + ''.join(
                '<svg class="w-4 h-4 text-amber-400 fill-current" viewBox="0 0 20 20">'
                '<path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462'
                'c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921'
                '-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838'
                '-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81'
                '.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>'
                for _ in range(5)
            )
            + '</div>'
        )
        Text(f'"{quote}"').className("text-gray-700 leading-relaxed text-sm")
        with Flex(align="center", gap=3):
            Avatar(name=name, size="sm")
            with Flex(direction="col", gap=0):
                Text(name).className("text-sm font-semibold text-gray-900")
                Text(role).className("text-xs text-gray-500")
    return card


# ── Landing Page ──────────────────────────────────────────────────────────────


class LandingPage(Page):
    title = "PyUI — Write Python. Render Anywhere."
    route = "/"
    layout = "full-width"

    def compose(self) -> None:  # noqa: PLR0915
        with Flex(direction="col", gap=0).className("min-h-screen bg-white"):

            # ── Navbar ────────────────────────────────────────────────────────
            with Flex(align="center", justify="between").className(
                "sticky top-0 z-50 bg-white/90 backdrop-blur-md "
                "border-b border-gray-100 px-8 py-4"
            ):
                # Logo
                with Flex(align="center", gap=2):
                    with Flex(align="center", justify="center").className(
                        "w-8 h-8 bg-gray-950 rounded-xl"
                    ):
                        Icon("code-2", size=16).className("text-white")
                    Text("PyUI").className(
                        "text-lg font-bold text-gray-950 tracking-tight"
                    )
                    Badge("v0.1.0", variant="secondary")

                # Nav links
                with Flex(align="center", gap=1).className("hidden md:flex"):
                    for label, href in [
                        ("Features", "#features"),
                        ("How it works", "#how-it-works"),
                        ("Components", "#components"),
                        ("Testimonials", "#testimonials"),
                    ]:
                        RawHTML(
                            f'<a href="{href}" class="px-3 py-1.5 text-sm font-medium '
                            f'text-gray-500 hover:text-gray-900 hover:bg-gray-50 '
                            f'rounded-lg transition-colors duration-150 no-underline">'
                            f'{label}</a>'
                        )

                # CTA
                with Flex(align="center", gap=2):
                    Button("View Storybook").style("ghost").size("sm")
                    Button("Get Started").style("primary").size("sm")

            # ── Hero ──────────────────────────────────────────────────────────
            with Flex(direction="col", align="center", justify="center").className(
                "px-6 pt-24 pb-20 text-center bg-gradient-to-b from-white to-gray-50/80"
            ):
                # Eyebrow badge
                with Flex(align="center", justify="center").className("mb-6"):
                    RawHTML(
                        '<span class="inline-flex items-center gap-2 px-3 py-1 '
                        'rounded-full bg-gray-950 text-white text-xs font-medium tracking-wide">'
                        '<span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>'
                        'Now in public beta — Phase 3 complete'
                        '</span>'
                    )

                # Headline
                RawHTML(
                    '<h1 class="text-5xl md:text-7xl font-extrabold tracking-[-0.04em] '
                    'leading-[0.95] text-gray-950 max-w-4xl mx-auto mb-6">'
                    'Write Python.<br>'
                    '<span class="bg-gradient-to-br from-violet-600 via-purple-600 to-indigo-600 '
                    'bg-clip-text text-transparent">Render Anywhere.</span>'
                    '</h1>'
                )

                Text(
                    "Build production-grade UIs in pure Python. "
                    "One codebase compiles to web, desktop, and terminal — "
                    "no HTML, no CSS, no JavaScript required."
                ).className(
                    "text-xl text-gray-500 leading-relaxed max-w-2xl mx-auto mb-10 font-light"
                ).paragraph()

                # CTA buttons
                with Flex(align="center", justify="center", gap=3).className("flex-wrap"):
                    Button("pip install pyui-framework").style("primary").size("lg").icon("terminal")
                    Button("View on GitHub").style("ghost").size("lg").icon("github")

                # Social proof
                with Flex(align="center", justify="center", gap=6).className("mt-12 flex-wrap"):
                    for value, label in [
                        ("42+", "Components"),
                        ("6", "Built-in Themes"),
                        ("3", "Render Targets"),
                        ("MIT", "License"),
                    ]:
                        with Flex(direction="col", align="center", gap=0):
                            Text(value).className(
                                "text-2xl font-bold text-gray-950 tracking-tight"
                            )
                            Text(label).className("text-xs text-gray-400 uppercase tracking-widest")

            # ── Code showcase ─────────────────────────────────────────────────
            with Flex(direction="col", align="center").className(
                "px-6 py-20 bg-gray-950"
            ).id("how-it-works"):
                with Container(size="xl"):
                    with Grid(cols=2, gap=12).className("items-center"):
                        # Left: explanation
                        with Flex(direction="col", gap=6):
                            Badge("How it works", variant="secondary")
                            RawHTML(
                                '<h2 class="text-4xl font-bold tracking-[-0.03em] '
                                'leading-[1.1] text-white">'
                                'Python classes.<br>'
                                '<span class="text-gray-400">Beautiful output.</span>'
                                '</h2>'
                            )
                            Text(
                                "Define your UI as Python classes. PyUI compiles them "
                                "through an Intermediate Representation into HTML, "
                                "native widgets, or terminal layouts."
                            ).className("text-gray-400 leading-relaxed").paragraph()

                            with Flex(direction="col", gap=3):
                                for step, desc in [
                                    ("1. Define", "Write App, Page, and Component classes in Python"),
                                    ("2. Compile", "PyUI builds a target-agnostic IR tree"),
                                    ("3. Render", "Output HTML, Qt widgets, or Rich TUI"),
                                ]:
                                    with Flex(align="center", gap=3):
                                        with Flex(align="center", justify="center").className(
                                            "w-7 h-7 rounded-lg bg-white/10 flex-shrink-0"
                                        ):
                                            Text(step.split(".")[0]).className(
                                                "text-xs font-bold text-white"
                                            )
                                        with Flex(direction="col", gap=0):
                                            Text(step).className(
                                                "text-sm font-semibold text-white"
                                            )
                                            Text(desc).className("text-xs text-gray-500")

                        # Right: code block
                        _code_block('''\
from pyui import App, Page, Button, Text, Flex, reactive

class MyApp(App):
    name  = "My App"
    theme = "dark"
    count = reactive(0)

class HomePage(Page):
    title = "Home"
    route = "/"

    def compose(self):
        with Flex(direction="col", gap=6).padding(10):
            Text(lambda: f"Count: {MyApp.count.get()}")

            with Flex(gap=4):
                Button("Increment").style("primary").onClick(
                    lambda: MyApp.count.set(
                        MyApp.count.get() + 1
                    )
                )
                Button("Reset").style("ghost").onClick(
                    lambda: MyApp.count.set(0)
                )

class App(App):
    home = HomePage()''')

            # Pipeline diagram
            with Flex(align="center", justify="center", gap=0).className("mt-16 flex-wrap"):
                for i, (icon_name, label) in enumerate([
                    ("code-2",      "Python Code"),
                    ("cpu",         "IR Compiler"),
                    ("globe",       "Web (HTML)"),
                    ("monitor",     "Desktop (Qt)"),
                    ("terminal",    "CLI (Rich)"),
                ]):
                    if i > 0:
                        Icon("chevron-right", size=16).className("text-gray-600 mx-2")
                    with Flex(direction="col", align="center", gap=2).className(
                        "bg-white/5 rounded-xl px-5 py-4 border border-white/10"
                    ):
                        Icon(icon_name, size=20).className("text-gray-300")
                        Text(label).className("text-xs text-gray-400 font-medium")

            # ── Features ──────────────────────────────────────────────────────
            with Flex(direction="col", align="center").className(
                "px-6 py-20"
            ).id("features"):
                pass

            # ── Stats bar ─────────────────────────────────────────────────────
            with Flex(align="center", justify="center", gap=0).className(
                "mt-16 bg-white/5 rounded-2xl border border-white/10 p-8 flex-wrap"
            ):
                for i, (val, label) in enumerate([
                    ("< 3s",   "Cold compile time"),
                    ("42+",    "Built-in components"),
                    ("6",      "Themes included"),
                    ("100%",   "Pure Python"),
                ]):
                    if i > 0:
                        Divider(direction="vertical")
                    with Flex(direction="col", align="center", gap=1).className("px-10"):
                        Text(val).className(
                            "text-3xl font-bold text-white tracking-tight"
                        )
                        Text(label).className("text-sm text-gray-400")

            # ── Features grid ─────────────────────────────────────────────────
            with Flex(direction="col", align="center").className(
                "px-6 py-20 bg-gray-50"
            ).id("features"):
                with Container(size="xl"):
                    with Flex(direction="col", align="center", gap=4).className(
                        "text-center mb-14"
                    ):
                        Badge("Features", variant="secondary")
                        Heading("Everything you need", level=2)
                        Text(
                            "A complete toolkit for building modern UIs — "
                            "from reactive state to production builds."
                        ).style("muted").paragraph()

                    with Grid(cols=3, gap=6):
                        _feature_card(
                            "zap", "Reactive State",
                            "Observable variables that auto-update the UI. "
                            "No boilerplate, no reducers — just Python."
                        )
                        _feature_card(
                            "layers", "42+ Components",
                            "Buttons, forms, tables, charts, modals, and more. "
                            "Every component is production-ready out of the box."
                        )
                        _feature_card(
                            "palette", "6 Built-in Themes",
                            "Light, dark, ocean, sunset, forest, rose. "
                            "Or define your own with a simple token dict."
                        )
                        _feature_card(
                            "globe", "Web Renderer",
                            "Compiles to clean HTML + Tailwind CSS + Alpine.js. "
                            "No build step, no webpack, no node_modules."
                        )
                        _feature_card(
                            "terminal", "CLI Toolchain",
                            "pyui run, pyui build, pyui storybook. "
                            "Everything you need from a single command."
                        )
                        _feature_card(
                            "shield-check", "Type Safe",
                            "Full type hints throughout. mypy strict mode passes. "
                            "Your IDE knows every prop and method."
                        )

            # ── Component showcase ────────────────────────────────────────────
            with Flex(direction="col", align="center").className(
                "px-6 py-20 bg-white"
            ).id("components"):
                with Container(size="xl"):
                    with Flex(direction="col", align="center", gap=4).className(
                        "text-center mb-14"
                    ):
                        Badge("Components", variant="secondary")
                        Heading("42+ ready-to-use components", level=2)
                        Text(
                            "Every component you need to build a real product."
                        ).style("muted").paragraph()

                    # Component category pills
                    with Flex(align="center", justify="center", gap=2, wrap=True).className("mb-10"):
                        for cat in [
                            "Layout", "Display", "Input", "Feedback",
                            "Navigation", "Data", "Media"
                        ]:
                            Badge(cat, variant="secondary")

                    # Live component previews
                    with Grid(cols=3, gap=6):
                        # Buttons card
                        with Flex(direction="col", gap=0).className(
                            "bg-white rounded-2xl border border-gray-100 overflow-hidden "
                            "shadow-[0_1px_3px_rgba(0,0,0,0.06)]"
                        ):
                            with Flex(align="center", justify="between").className(
                                "px-5 py-3 border-b border-gray-100 bg-gray-50/50"
                            ):
                                Text("Buttons").className(
                                    "text-[11px] font-semibold text-gray-500 uppercase tracking-wide"
                                )
                                Badge("7 variants", variant="secondary")
                            with Flex(align="center", gap=2, wrap=True).className("p-5"):
                                Button("Primary").style("primary").size("sm")
                                Button("Ghost").style("ghost").size("sm")
                                Button("Danger").style("danger").size("sm")
                                Button("Success").style("success").size("sm")
                                Button("Gradient").style("gradient").size("sm")

                        # Stats card
                        with Flex(direction="col", gap=0).className(
                            "bg-white rounded-2xl border border-gray-100 overflow-hidden "
                            "shadow-[0_1px_3px_rgba(0,0,0,0.06)]"
                        ):
                            with Flex(align="center", justify="between").className(
                                "px-5 py-3 border-b border-gray-100 bg-gray-50/50"
                            ):
                                Text("Stats").className(
                                    "text-[11px] font-semibold text-gray-500 uppercase tracking-wide"
                                )
                                Badge("Trend indicators", variant="secondary")
                            with Grid(cols=2, gap=4).className("p-5"):
                                Stat("Users", "24.5k", trend="+18%", trend_up=True)
                                Stat("Revenue", "$84k", trend="+6%", trend_up=True)
                                Stat("Churn", "2.4%", trend="-0.8%", trend_up=False)
                                Stat("Uptime", "99.9%", trend="+0.1%", trend_up=True)

                        # Badges card
                        with Flex(direction="col", gap=0).className(
                            "bg-white rounded-2xl border border-gray-100 overflow-hidden "
                            "shadow-[0_1px_3px_rgba(0,0,0,0.06)]"
                        ):
                            with Flex(align="center", justify="between").className(
                                "px-5 py-3 border-b border-gray-100 bg-gray-50/50"
                            ):
                                Text("Badges & Avatars").className(
                                    "text-[11px] font-semibold text-gray-500 uppercase tracking-wide"
                                )
                                Badge("Display", variant="secondary")
                            with Flex(direction="col", gap=4).className("p-5"):
                                with Flex(align="center", gap=2, wrap=True):
                                    Badge("Primary", variant="primary")
                                    Badge("Success", variant="success")
                                    Badge("Warning", variant="warning")
                                    Badge("Danger", variant="danger")
                                with Flex(align="center", gap=2):
                                    Avatar(name="Alice Smith", size="sm")
                                    Avatar(name="Bob Jones", size="sm")
                                    Avatar(name="Carol White", size="sm")
                                    Avatar(name="Dan Brown", size="sm")
                                    Avatar(name="Eve Davis", size="sm")

            # ── Testimonials ──────────────────────────────────────────────────
            with Flex(direction="col", align="center").className(
                "px-6 py-20 bg-gray-50"
            ).id("testimonials"):
                with Container(size="xl"):
                    with Flex(direction="col", align="center", gap=4).className(
                        "text-center mb-14"
                    ):
                        Badge("Testimonials", variant="secondary")
                        Heading("Loved by Python developers", level=2)

                    with Grid(cols=3, gap=6):
                        _testimonial(
                            "I built our entire internal dashboard in a weekend. "
                            "No frontend dev needed — just Python.",
                            "Sarah Chen", "Data Scientist @ Stripe",
                            "SC"
                        )
                        _testimonial(
                            "Finally a UI framework that doesn't make me learn "
                            "a whole new ecosystem. It just works.",
                            "Marcus Webb", "Backend Engineer @ Vercel",
                            "MW"
                        )
                        _testimonial(
                            "The storybook is incredible. I can see every component "
                            "live before I use it. Game changer.",
                            "Priya Nair", "ML Engineer @ Anthropic",
                            "PN"
                        )

            # ── CTA section ───────────────────────────────────────────────────
            with Flex(direction="col", align="center", justify="center").className(
                "px-6 py-24 bg-gray-950 text-center"
            ):
                RawHTML(
                    '<h2 class="text-4xl md:text-5xl font-extrabold tracking-[-0.03em] '
                    'text-white mb-4 max-w-2xl mx-auto">'
                    'Start building in minutes.'
                    '</h2>'
                )
                Text(
                    "Install PyUI, run the storybook, and ship your first UI today."
                ).className("text-gray-400 text-lg mb-10 font-light").paragraph()

                _code_block("pip install pyui-framework\npyui storybook")

                with Flex(align="center", justify="center", gap=3).className("mt-8 flex-wrap"):
                    Button("Read the Docs").style("ghost").size("lg").icon("book-open")
                    Button("View on GitHub").style("primary").size("lg").icon("github")

            # ── Footer ────────────────────────────────────────────────────────
            with Flex(align="center", justify="between").className(
                "px-8 py-6 border-t border-gray-100 bg-white flex-wrap gap-4"
            ):
                with Flex(align="center", gap=2):
                    with Flex(align="center", justify="center").className(
                        "w-6 h-6 bg-gray-950 rounded-lg"
                    ):
                        Icon("code-2", size=12).className("text-white")
                    Text("PyUI").className("text-sm font-semibold text-gray-900")
                    Text("·").className("text-gray-300")
                    Text("MIT License").className("text-sm text-gray-400")
                    Text("·").className("text-gray-300")
                    Text("v0.1.0").className("text-sm text-gray-400")

                Text(
                    "Built with pure Python. No HTML. No JavaScript."
                ).className("text-sm text-gray-400")


class LandingApp(App):
    name = "PyUI"
    description = "Write Python. Render Anywhere."
    theme = "light"
    home = LandingPage()

if __name__ == "__main__":
    import sys
    sys.path.insert(0, "src")
    from pyui.server.dev_server import run_dev_server
    run_dev_server(LandingApp, port=8001, open_browser=True)
