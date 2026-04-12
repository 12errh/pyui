from pyui import (
    Alert,
    App,
    Avatar,
    Badge,
    Button,
    Chart,
    Checkbox,
    DatePicker,
    Divider,
    FilePicker,
    Flex,
    Form,
    Grid,
    Heading,
    Icon,
    Input,
    Markdown,
    Page,
    Progress,
    Select,
    Skeleton,
    Slider,
    Spinner,
    Stack,
    Stat,
    Table,
    Tag,
    Text,
    Toggle,
    Tooltip,
)


class StorybookPage(Page):
    title = "PyUI Storybook - Component Gallery"
    route = "/"
    def compose(self) -> None:
        with Flex(direction="col", gap=10).padding(10):
            Heading("PyUI Storybook", subtitle="Component Gallery & UI Kit").style("gradient")

            with Stack(spacing=12):
                # ── Layout ──
                self._section("Layout & Structure")
                with Grid(cols=2, gap=6):
                    with Stack(spacing=4):
                        Text("Flex / Stack").style("muted")
                        with Flex(gap=4).className("p-4 border rounded"):
                            Button("Item 1")
                            Button("Item 2")
                    with Stack(spacing=4):
                        Text("Grid").style("muted")
                        with Grid(cols=3, gap=2).className("p-4 border rounded"):
                            for i in range(3):
                                Button(f"G{i}")

                # ── Display ──
                self._section("Display & Content")
                with Flex(gap=4, wrap=True):
                    Badge("Beta", variant="primary")
                    Badge("Live", variant="success")
                    Tag("Design")
                    Tag("Dev", variant="primary")
                    Avatar(name="John Doe")
                    Avatar(
                        src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=128&h=128&fit=crop"
                    )
                    Icon("cpu", color="violet-600")

                with Stack(spacing=4):
                    Text("Markdown").style("muted")
                    Markdown("### Hello World\nThis is **markdown** rendered by `marked.js`.")

                # ── Inputs ──
                self._section("Inputs & Forms")
                with Form(title="Registration"):
                    Input(placeholder="Username", label="Username")
                    Input(type="password", placeholder="Password", label="Password")
                    Select(
                        options=[("us", "United States"), ("uk", "United Kingdom")], label="Country"
                    )
                    with Flex(gap=6):
                        Checkbox(label="Remember me")
                        Toggle(label="Dark mode")
                    Slider(label="Volume", value=50)
                    DatePicker(label="Birthday")
                    FilePicker(label="Resume")
                    Button("Submit").style("primary").width("full")

                # ── Feedback ──
                self._section("Feedback & Overlays")
                with Stack(spacing=4):
                    Alert("System Update", "A new version of PyUI is available.", variant="info")
                    with Flex(gap=6):
                        Spinner(size="lg")
                        Progress(value=65)
                    with Flex(gap=4):
                        Skeleton(variant="circle")
                        with Stack(spacing=2):
                            Skeleton()
                            Skeleton()
                    with Tooltip("This is helpful info"):
                        Button("Hover for Tooltip")

                # ── Data ──
                self._section("Data & Visualization")
                with Grid(cols=3, gap=4):
                    Stat("Users", "2,543", trend="+12.5%", trend_up=True)
                    Stat("Revenue", "$12.4k", trend="-3.2%", trend_up=False)
                    Stat("Uptime", "99.9%")

                with Grid(cols=2, gap=6):
                    Table(
                        headers=["Name", "Role", "Status"],
                        rows=[
                            ["Alice", "Admin", "Active"],
                            ["Bob", "User", "Away"],
                            ["Charlie", "User", "Active"],
                        ],
                    ).striped()
                    Chart(
                        type="line",
                        labels=["Jan", "Feb", "Mar", "Apr"],
                        datasets=[
                            {
                                "label": "Sales",
                                "data": [400, 300, 600, 500],
                                "borderColor": "rgb(124, 58, 237)",
                            }
                        ],
                    )

    def _section(self, title: str) -> None:
        with Stack(spacing=2).className("mt-8 mb-4"):
            Heading(title, level=2)
            Divider()


class StorybookApp(App):
    name = "PyUI Storybook"
    index = StorybookPage()


def run_storybook(port: int = 8000, open_browser: bool = True) -> None:
    from pyui.server.dev_server import run_dev_server

    run_dev_server(StorybookApp, port=port, open_browser=open_browser)
