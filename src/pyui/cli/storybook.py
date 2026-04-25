from pyui import (
    Alert,
    App,
    Avatar,
    Badge,
    Breadcrumb,
    Button,
    Chart,
    Checkbox,
    DatePicker,
    Divider,
    Drawer,
    FilePicker,
    Flex,
    Form,
    Grid,
    Heading,
    Icon,
    Input,
    Markdown,
    Menu,
    Modal,
    Nav,
    Pagination,
    Page,
    Progress,
    Radio,
    Select,
    Skeleton,
    Slider,
    Spacer,
    Spinner,
    Stack,
    Stat,
    Table,
    Tag,
    Tabs,
    Text,
    Textarea,
    Toggle,
    Tooltip,
)

# ── Sidebar nav items ──────────────────────────────────────────────────────────
_NAV = [
    ("Foundation", [
        ("zap",                  "Typography",      "typography"),
        ("tag",                  "Badges + Tags",   "badges"),
        ("user-circle",          "Avatars + Icons", "avatars"),
    ]),
    ("Inputs", [
        ("mouse-pointer-click",  "Buttons",         "buttons"),
        ("text-cursor-input",    "Text Inputs",     "inputs"),
        ("sliders",              "Controls",        "controls"),
        ("circle-dot",           "Radio",           "radio"),
        ("file-text",            "Forms",           "forms"),
    ]),
    ("Feedback", [
        ("alert-circle",         "Alerts",          "alerts"),
        ("layers",               "Overlays",        "overlays"),
        ("loader",               "Loading States",  "loading"),
    ]),
    ("Navigation", [
        ("navigation",           "Nav + Tabs",      "nav"),
        ("arrow-left-right",     "Pagination",      "pagination"),
        ("list",                 "Menu",            "menu"),
    ]),
    ("Data", [
        ("bar-chart-2",          "Stats",           "stats"),
        ("table-2",              "Tables",          "tables"),
        ("activity",             "Charts",          "charts"),
    ]),
]


class StorybookPage(Page):
    title = "PyUI Storybook — Component Gallery"
    route = "/"
    layout = "full-width"

    def compose(self) -> None:
        # Root: sidebar fixed-width + main flex-1, small padding from edges
        with Flex(direction="row", align="start", gap=0).className(
            "min-h-screen bg-[#f7f7f8] pl-3"
        ):
            self._sidebar()
            self._main()

    # =========================================================
    # SIDEBAR — fixed, no excess padding, scroll-spy aware
    # =========================================================
    def _sidebar(self) -> None:
        with Flex(direction="col", align="start", gap=0).className(
            "w-[220px] flex-shrink-0 bg-white border border-gray-100 rounded-xl "
            "h-[calc(100vh-24px)] sticky top-3 overflow-y-auto self-start "
            "shadow-[0_1px_4px_rgba(0,0,0,0.04)] mt-3 mb-3"
        ):
            # Logo
            with Flex(align="center", gap=2).className(
                "px-4 py-5 flex-shrink-0"
            ):
                with Flex(align="center", justify="center").className(
                    "w-7 h-7 bg-gray-950 rounded-lg flex-shrink-0"
                ):
                    Icon("code-2", size=12).className("text-white")
                with Flex(direction="col", gap=0):
                    Text("PyUI").className(
                        "text-[13px] font-bold text-gray-950 tracking-tight leading-none"
                    )
                    Text("Storybook").className(
                        "text-[9px] text-gray-400 uppercase tracking-widest"
                    )

            # Nav groups — use RawHTML for proper anchor links with scroll behavior
            for group_label, items in _NAV:
                Text(group_label).className(
                    "block px-4 pt-4 pb-1 text-[9px] font-semibold "
                    "uppercase tracking-widest text-gray-400"
                )
                for icon_name, label, anchor in items:
                    from pyui.components.display.rawhtml import RawHTML
                    RawHTML(
                        f'<a href="#{anchor}" '
                        f'id="sb-link-{anchor}" '
                        f'class="flex items-center gap-2 px-4 py-[7px] text-[13px] font-medium '
                        f'text-gray-500 hover:text-gray-900 hover:bg-gray-50 cursor-pointer '
                        f'transition-all duration-150 border-l-2 border-transparent '
                        f'hover:border-gray-300 sb-nav-link no-underline" '
                        f'onclick="event.preventDefault(); '
                        f'document.getElementById(\'{anchor}\')?.scrollIntoView({{behavior:\'smooth\'}})">'
                        f'<i data-lucide="{icon_name}" style="width:13px;height:13px;flex-shrink:0"></i>'
                        f'<span>{label}</span>'
                        f'</a>'
                    )

    # =========================================================
    # MAIN — zero side padding on wrapper, sections handle own padding
    # =========================================================
    def _main(self) -> None:
        with Flex(direction="col", gap=0).className("flex-1 min-w-0 min-h-screen"):
            # Content area
            with Flex(direction="col", gap=0).className("px-8 py-10 pb-24 w-full"):
                # Page title — inline, no box
                with Flex(align="center", justify="between").className("mb-8"):
                    with Flex(align="center", gap=3):
                        Heading("Component Gallery", level=2)
                        Badge("42+ Components", variant="secondary")
                    with Flex(align="center", gap=2):
                        Badge("Alpine.js", variant="dark")
                        Badge("Tailwind", variant="dark")
                        Badge("Chart.js", variant="dark")
                # Hero intro
                Text(
                    "Every PyUI component, live and interactive. "
                    "Built entirely with pure Python — no HTML, no templates."
                ).style("muted").paragraph()

                self._section_typography()
                self._section_badges()
                self._section_avatars()
                self._section_buttons()
                self._section_inputs()
                self._section_controls()
                self._section_radio()
                self._section_forms()
                self._section_alerts()
                self._section_overlays()
                self._section_loading()
                self._section_nav()
                self._section_pagination()
                self._section_menu()
                self._section_stats()
                self._section_tables()
                self._section_charts()

    # =========================================================
    # HELPERS
    # =========================================================
    def _section_header(self, title: str, desc: str, anchor: str) -> None:
        """Section title with scroll-spy anchor."""
        with Flex(direction="col", gap=1).className(
            "mt-14 mb-5 first:mt-0 sb-section-anchor"
        ).id(anchor):
            Heading(title, level=2)
            Text(desc).style("muted").paragraph()

    def _card_wrap(self, label: str, hint: str = "") -> Flex:
        """Preview card outer shell — label floats inline, no box header."""
        card = Flex(direction="col", gap=0).className(
            "bg-white border border-gray-100 rounded-2xl overflow-hidden "
            "shadow-[0_1px_4px_rgba(0,0,0,0.04)] hover:shadow-[0_4px_24px_rgba(0,0,0,0.07)] "
            "transition-all duration-300 mb-5"
        )
        with card:
            with Flex(align="center", justify="between").className(
                "px-5 pt-4 pb-0"
            ):
                Text(label).className(
                    "text-[10px] font-semibold text-gray-400 tracking-[0.12em] uppercase"
                )
                if hint:
                    Badge(hint, variant="secondary")
        return card

    def _pad(self) -> Flex:
        """Standard padded content area inside a card."""
        return Flex(direction="col", gap=5).className("px-5 pt-3 pb-6")

    def _row(self) -> Flex:
        """Horizontal flex row inside a card."""
        return Flex(align="center", gap=3, wrap=True).className("px-5 pt-3 pb-6")

    # =========================================================
    # TYPOGRAPHY
    # =========================================================
    def _section_typography(self) -> None:
        self._section_header("Typography",
            "Headings h1–h6, text variants, and style modifiers.", "typography")
        with Grid(cols=2, gap=5):
            with self._card_wrap("Headings", "h1 – h4"):
                with self._pad():
                    Heading("Display Heading", level=1)
                    Heading("Section Heading", level=2)
                    Heading("Card Title", level=3)
                    Heading("Subsection", level=4)
            with self._card_wrap("Text Variants", "6 variants"):
                with self._pad():
                    Text("Default — primary body text").paragraph()
                    Text("Lead — intro paragraph").style("lead").paragraph()
                    Text("Muted — secondary copy").style("muted").paragraph()
                    Text("Small — captions").style("small").paragraph()
                    Text("Success — positive state").style("success").paragraph()
                    Text("Error — validation").style("error").paragraph()
        with self._card_wrap("Heading Style Variants", "gradient · display · muted · mono"):
            with self._pad():
                Heading("Gradient Heading", level=2).style("gradient")
                Heading("Display Heading", level=2).style("display")
                Heading("Muted Heading",   level=2).style("muted")
                Heading("Mono Heading",    level=2).style("mono")

    # =========================================================
    # BADGES + TAGS
    # =========================================================
    def _section_badges(self) -> None:
        self._section_header("Badges + Tags",
            "Status indicators, labels, and categorization chips.", "badges")
        with Grid(cols=2, gap=5):
            with self._card_wrap("Badge", "7 variants"):
                with self._row():
                    Badge("Primary",   variant="primary")
                    Badge("Secondary", variant="secondary")
                    Badge("Success",   variant="success")
                    Badge("Danger",    variant="danger")
                    Badge("Warning",   variant="warning")
                    Badge("Info",      variant="info")
                    Badge("Dark",      variant="dark")
            with self._card_wrap("Tag", "4 variants + closable"):
                with self._row():
                    Tag("Design",   variant="primary")
                    Tag("Frontend", variant="secondary")
                    Tag("Shipped",  variant="success")
                    Tag("Blocked",  variant="danger")
                    Tag("Closable", variant="secondary").closable()

    # =========================================================
    # AVATARS + ICONS
    # =========================================================
    def _section_avatars(self) -> None:
        self._section_header("Avatars + Icons",
            "User representations and the Lucide icon library.", "avatars")
        with Grid(cols=2, gap=5):
            with self._card_wrap("Avatar", "6 sizes"):
                with self._row():
                    Avatar(name="Alice Smith", size="xs")
                    Avatar(name="Bob Jones",   size="sm")
                    Avatar(name="Carol White", size="md")
                    Avatar(name="Dan Brown",   size="lg")
                    Avatar(src="https://i.pravatar.cc/150?img=3", name="Eve", size="xl")
                    Avatar(src="https://i.pravatar.cc/150?img=7", name="Frank", size="2xl")
            with self._card_wrap("Icon", "Lucide CDN"):
                with self._row():
                    for name in ["zap","layers","cpu","globe","shield-check",
                                 "rocket","sparkles","terminal","git-branch",
                                 "package","code-2","database","lock","mail","bell"]:
                        Icon(name, size=20).className("text-gray-700")

    # =========================================================
    # BUTTONS
    # =========================================================
    def _section_buttons(self) -> None:
        self._section_header("Buttons",
            "Every variant, size, and state — the primary action primitive.", "buttons")
        with self._card_wrap("Variants", "7 variants"):
            with self._row():
                Button("Primary").style("primary")
                Button("Secondary").style("secondary")
                Button("Ghost").style("ghost")
                Button("Danger").style("danger")
                Button("Success").style("success")
                Button("Gradient").style("gradient")
                Button("Link").style("link")
        with self._card_wrap("Sizes", "xs → xl"):
            with self._row():
                Button("XSmall").style("primary").size("xs")
                Button("Small").style("primary").size("sm")
                Button("Medium").style("primary").size("md")
                Button("Large").style("primary").size("lg")
                Button("XLarge").style("primary").size("xl")
        with self._card_wrap("States + Icons"):
            with self._row():
                Button("Default").style("primary")
                Button("Loading").style("primary").loading(True)
                Button("Disabled").style("primary").disabled(True)
                Button("With Icon").style("ghost").icon("zap")
                Button("Icon Right").style("secondary").icon("arrow-right", "right")
                Button("Ghost Icon").style("ghost").icon("settings")

    # =========================================================
    # TEXT INPUTS
    # =========================================================
    def _section_inputs(self) -> None:
        self._section_header("Text Inputs",
            "Input, Textarea, Select, DatePicker, FilePicker.", "inputs")
        with Grid(cols=2, gap=5):
            with self._card_wrap("Input", "4 types"):
                with self._pad():
                    Input(placeholder="Default input",       label="Username")
                    Input(type="email",    placeholder="you@example.com", label="Email")
                    Input(type="password", placeholder="Min 8 characters", label="Password")
                    Input(placeholder="Search…",        label="Search")
            with self._card_wrap("Textarea + Select + Pickers"):
                with self._pad():
                    Textarea(placeholder="Write something…", label="Bio", rows=3)
                    Select(options=[
                        ("us","United States"),("uk","United Kingdom"),
                        ("de","Germany"),("jp","Japan"),
                    ], label="Country")
                    DatePicker(label="Date of Birth")
                    FilePicker(label="Upload Resume")

    # =========================================================
    # CONTROLS
    # =========================================================
    def _section_controls(self) -> None:
        self._section_header("Controls",
            "Checkbox, Toggle, and Slider — binary and range inputs.", "controls")
        with Grid(cols=2, gap=5):
            with self._card_wrap("Checkbox + Toggle"):
                with self._pad():
                    Checkbox(label="Accept terms and conditions")
                    Checkbox(label="Subscribe to newsletter", checked=True)
                    Checkbox(label="Disabled option").disabled(True)
                    Divider()
                    Toggle(label="Enable notifications")
                    Toggle(label="Dark mode", checked=True)
                    Toggle(label="Auto-save", checked=True)
            with self._card_wrap("Slider", "range input"):
                with self._pad():
                    Slider(label="Volume",     value=60)
                    Slider(label="Brightness", value=80)
                    Slider(label="Opacity",    value=40)
                    Slider(label="Scale",      value=20)

    # =========================================================
    # RADIO
    # =========================================================
    def _section_radio(self) -> None:
        self._section_header("Radio",
            "Single-selection radio button groups.", "radio")
        with Grid(cols=2, gap=5):
            with self._card_wrap("Radio Group", "3 options"):
                with self._pad():
                    Radio(
                        options=[
                            ("free",    "Free — $0/month"),
                            ("pro",     "Pro — $12/month"),
                            ("team",    "Team — $49/month"),
                        ],
                        value="pro",
                        label="Billing Plan",
                    )
            with self._card_wrap("Radio Group", "4 options"):
                with self._pad():
                    Radio(
                        options=[
                            ("web",     "Web"),
                            ("desktop", "Desktop"),
                            ("cli",     "CLI"),
                            ("all",     "All targets"),
                        ],
                        value="web",
                        label="Render Target",
                    )

    # =========================================================
    # FORMS
    # =========================================================
    def _section_forms(self) -> None:
        self._section_header("Forms",
            "Structured form containers with labels and validation.", "forms")
        with Grid(cols=2, gap=5):
            with Form(title="Create Account"):
                Input(placeholder="John Doe",          label="Full Name")
                Input(type="email", placeholder="you@example.com", label="Email")
                Input(type="password", placeholder="Min 8 characters", label="Password")
                Select(options=[
                    ("dev","Developer"),("design","Designer"),("pm","Product Manager")
                ], label="Role")
                Checkbox(label="I agree to the Terms of Service")
                Button("Create Account").style("primary")
            with Form(title="Contact Us"):
                Input(placeholder="Your name",         label="Name")
                Input(type="email", placeholder="your@email.com", label="Email")
                Select(options=[
                    ("bug","Bug Report"),("feature","Feature Request"),("other","Other")
                ], label="Subject")
                Textarea(placeholder="Describe your issue…", label="Message", rows=4)
                Toggle(label="Send me a copy")
                Button("Send Message").style("primary")

    # =========================================================
    # ALERTS
    # =========================================================
    def _section_alerts(self) -> None:
        self._section_header("Alerts",
            "Inline status messages with left-accent border design.", "alerts")
        with Flex(direction="col", gap=3):
            Alert("Information",
                  "This is an informational message. Use it for neutral updates.",
                  variant="info")
            Alert("Success",
                  "Your changes have been saved successfully.",
                  variant="success")
            Alert("Warning",
                  "Your trial expires in 3 days. Upgrade to keep access.",
                  variant="warning")
            Alert("Error",
                  "Failed to connect to the server. Please try again.",
                  variant="danger")

    # =========================================================
    # OVERLAYS
    # =========================================================
    def _section_overlays(self) -> None:
        self._section_header("Overlays",
            "Modal, Drawer, and Tooltip — focused interaction layers.", "overlays")
        with Grid(cols=2, gap=5):
            with self._card_wrap("Modal", "Alpine.js"):
                with self._pad():
                    Text("Modals use Alpine.js for open/close state.").style("muted").paragraph()
                    from pyui.components.display.rawhtml import RawHTML
                    RawHTML(
                        '<div x-data="{ open: false }">'
                        '<button @click="open = true" class="inline-flex items-center justify-center gap-2 font-medium tracking-tight '
                        'transition-all duration-200 ease-out focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 '
                        'select-none cursor-pointer active:scale-[0.97] h-9 px-4 text-sm rounded-lg '
                        'bg-gray-950 text-white shadow-sm hover:bg-gray-800 hover:shadow-md hover:-translate-y-px focus-visible:ring-gray-950">'
                        'Open Modal</button>'
                        '<template x-if="open">'
                        '<div class="fixed inset-0 z-50 flex items-center justify-center p-4">'
                        '<div class="fixed inset-0 bg-gray-950/60 backdrop-blur-sm z-40 transition-opacity duration-200" @click="open = false" x-transition.opacity></div>'
                        '<div class="relative w-full max-w-lg bg-white rounded-2xl shadow-[0_25px_60px_rgba(0,0,0,0.15)] border border-gray-100 overflow-hidden z-10" @click.stop x-transition>'
                        '<div class="flex items-center justify-between px-6 pt-6 pb-4 border-b border-gray-100">'
                        '<h3 class="text-base font-semibold text-gray-900 tracking-tight">Confirm Action</h3>'
                        '<button @click="open = false" class="text-gray-400 hover:text-gray-600 transition-colors rounded-lg p-1 hover:bg-gray-100">'
                        '<i data-lucide="x" style="width:16px;height:16px" x-init="lucide.createIcons()"></i></button>'
                        '</div>'
                        '<div class="px-6 py-5"><p class="text-gray-700 leading-relaxed">Are you sure? This action cannot be undone.</p></div>'
                        '<div class="bg-gray-50 px-6 py-4 flex flex-row-reverse gap-3 border-t border-gray-100">'
                        '<button @click="open = false" class="inline-flex items-center justify-center gap-2 font-medium tracking-tight transition-all duration-200 ease-out h-9 px-4 text-sm rounded-lg bg-gray-950 text-white shadow-sm hover:bg-gray-800">Confirm</button>'
                        '<button @click="open = false" class="inline-flex items-center justify-center gap-2 font-medium tracking-tight transition-all duration-200 ease-out h-9 px-4 text-sm rounded-lg border border-gray-200 bg-white text-gray-700 shadow-sm hover:bg-gray-50">Cancel</button>'
                        '</div>'
                        '</div>'
                        '</div>'
                        '</template>'
                        '</div>'
                    )
            with self._card_wrap("Drawer", "side=right"):
                with self._pad():
                    Text("Drawers slide in from the side.").style("muted").paragraph()
                    from pyui.components.display.rawhtml import RawHTML
                    RawHTML(
                        '<div x-data="{ open: false }">'
                        '<button @click="open = true" class="inline-flex items-center justify-center gap-2 font-medium tracking-tight '
                        'transition-all duration-200 ease-out focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 '
                        'select-none cursor-pointer active:scale-[0.97] h-9 px-4 text-sm rounded-lg '
                        'border border-gray-200 bg-white text-gray-700 shadow-sm hover:bg-gray-50 hover:border-gray-300 hover:-translate-y-px focus-visible:ring-gray-300">'
                        'Open Drawer</button>'
                        '<template x-if="open">'
                        '<div class="fixed inset-0 z-50">'
                        '<div class="fixed inset-0 bg-gray-950/50 backdrop-blur-sm z-40 transition-opacity duration-300" @click="open = false" x-transition.opacity></div>'
                        '<div class="fixed inset-y-0 right-0 w-full max-w-md bg-white z-50 shadow-[0_0_60px_rgba(0,0,0,0.15)] flex flex-col transition-transform duration-300 ease-out" '
                        'x-transition:enter="transform transition ease-out duration-300" '
                        'x-transition:enter-start="translate-x-full" '
                        'x-transition:enter-end="translate-x-0">'
                        '<div class="flex items-center justify-between px-6 py-5 border-b border-gray-100">'
                        '<h2 class="text-base font-semibold text-gray-900 tracking-tight">Settings</h2>'
                        '<button @click="open = false" class="text-gray-400 hover:text-gray-600 transition-colors rounded-lg p-1 hover:bg-gray-100">'
                        '<i data-lucide="x" style="width:16px;height:16px" x-init="lucide.createIcons()"></i></button>'
                        '</div>'
                        '<div class="flex-1 px-6 py-6 overflow-y-auto"><p class="text-gray-700 leading-relaxed">Drawer content goes here.</p></div>'
                        '</div>'
                        '</div>'
                        '</template>'
                        '</div>'
                    )
        with self._card_wrap("Tooltip", "group-hover"):
            with Flex(align="center", gap=6).className("px-5 py-5"):
                with Tooltip("This is a helpful tooltip"):
                    Button("Hover me").style("ghost")
                with Tooltip("Saved to clipboard!"):
                    Button("Copy code").style("secondary").icon("copy")
                with Tooltip("Opens in new tab"):
                    Button("Docs").style("link").icon("external-link", "right")

    # =========================================================
    # LOADING STATES — fixed spinner rendering
    # =========================================================
    def _section_loading(self) -> None:
        self._section_header("Loading States",
            "Spinner, Progress, and Skeleton for async content.", "loading")
        with Grid(cols=3, gap=5):
            # Spinner — explicit sizes shown side by side
            with self._card_wrap("Spinner", "5 sizes"):
                with Flex(align="center", justify="center", gap=5).className("px-5 py-10"):
                    Spinner(size="xs")
                    Spinner(size="sm")
                    Spinner(size="md")
                    Spinner(size="lg")
                    Spinner(size="xl")

            # Progress bars
            with self._card_wrap("Progress", "0 – 100%"):
                with self._pad():
                    with Flex(direction="col", gap=3):
                        with Flex(align="center", justify="between"):
                            Text("Uploading").style("small")
                            Text("25%").style("small")
                        Progress(value=25)
                    with Flex(direction="col", gap=3):
                        with Flex(align="center", justify="between"):
                            Text("Processing").style("small")
                            Text("60%").style("small")
                        Progress(value=60)
                    with Flex(direction="col", gap=3):
                        with Flex(align="center", justify="between"):
                            Text("Complete").style("small")
                            Text("100%").style("small")
                        Progress(value=100)

            # Skeleton
            with self._card_wrap("Skeleton", "shimmer"):
                with self._pad():
                    with Flex(align="center", gap=3):
                        Skeleton(variant="circle").className("w-10 h-10 flex-shrink-0")
                        with Flex(direction="col", gap=2).className("flex-1"):
                            Skeleton().className("h-3 w-3/4")
                            Skeleton().className("h-3 w-1/2")
                    Skeleton(variant="rect").className("h-20 w-full")
                    with Flex(direction="col", gap=2):
                        Skeleton().className("h-3 w-full")
                        Skeleton().className("h-3 w-5/6")
                        Skeleton().className("h-3 w-4/6")

    # =========================================================
    # NAV + TABS + BREADCRUMB
    # =========================================================
    def _section_nav(self) -> None:
        self._section_header("Nav + Tabs + Breadcrumb",
            "Navigation primitives for routing and content switching.", "nav")
        with Flex(direction="col", gap=5):
            with self._card_wrap("Nav", "horizontal links"):
                with Flex(align="center", justify="between").className("px-5 py-4"):
                    Nav(items=[
                        ("Home","/"),("Products","/products"),
                        ("Pricing","/pricing"),("Docs","/docs"),("Blog","/blog"),
                    ])
                    Button("Sign In").style("ghost").size("sm")
            with self._card_wrap("Tabs", "Alpine.js switcher"):
                with Flex(direction="col", gap=0).className("px-5 py-4"):
                    Tabs(active_tab="Overview").add_tab(
                        "Overview",
                        Text("Overview content — summary and key metrics.").paragraph(),
                    ).add_tab(
                        "Analytics",
                        Text("Analytics content — charts and data.").paragraph(),
                    ).add_tab(
                        "Settings",
                        Text("Settings content — configuration options.").paragraph(),
                    )
            with self._card_wrap("Breadcrumb", "path navigation"):
                with self._pad():
                    Breadcrumb(items=[
                        ("Home","/"),("Components","/components"),
                        ("Navigation","/components/navigation"),
                    ])
                    Breadcrumb(items=[
                        ("Dashboard","/"),("Projects","/projects"),
                        ("PyUI","/projects/pyui"),("Settings","/projects/pyui/settings"),
                    ])

    # =========================================================
    # PAGINATION
    # =========================================================
    def _section_pagination(self) -> None:
        self._section_header("Pagination",
            "Page controls for navigating large datasets.", "pagination")
        with self._card_wrap("Pagination", "current / total"):
            with self._pad():
                Pagination(current=1,  total=10)
                Pagination(current=5,  total=10)
                Pagination(current=10, total=10)

    # =========================================================
    # MENU
    # =========================================================
    def _section_menu(self) -> None:
        self._section_header("Menu",
            "Contextual dropdown menus for actions and navigation.", "menu")
        with Grid(cols=3, gap=5):
            with self._card_wrap("Actions"):
                with Flex(align="center", justify="center").className("px-5 py-5"):
                    Menu(items=[
                        ("Edit","/edit"),("Duplicate","/dup"),
                        ("Archive","/arch"),("Delete","/del"),
                    ])
            with self._card_wrap("User"):
                with Flex(align="center", justify="center").className("px-5 py-5"):
                    Menu(items=[
                        ("Profile","/profile"),("Settings","/settings"),
                        ("Billing","/billing"),("Sign Out","/logout"),
                    ])
            with self._card_wrap("View"):
                with Flex(align="center", justify="center").className("px-5 py-5"):
                    Menu(items=[
                        ("List View","/list"),("Grid View","/grid"),
                        ("Board View","/board"),("Calendar","/cal"),
                    ])

    # =========================================================
    # STATS
    # =========================================================
    def _section_stats(self) -> None:
        self._section_header("Stats",
            "Key metric cards with trend indicators.", "stats")
        with Grid(cols=4, gap=5):
            Stat("Total Users",    "24,521", trend="+18.2%", trend_up=True)
            Stat("Monthly Revenue","$84.2k", trend="+6.1%",  trend_up=True)
            Stat("Churn Rate",     "2.4%",   trend="-0.8%",  trend_up=False)
            Stat("Uptime",         "99.98%", trend="+0.01%", trend_up=True)
        with Grid(cols=3, gap=5).className("mt-4"):
            Stat("Active Sessions","1,204",  trend="+42",    trend_up=True)
            Stat("Avg. Response",  "142ms",  trend="-18ms",  trend_up=True)
            Stat("Error Rate",     "0.03%",  trend="-0.01%", trend_up=True)

    # =========================================================
    # TABLES
    # =========================================================
    def _section_tables(self) -> None:
        self._section_header("Tables",
            "Structured data grids with striped rows and hover states.", "tables")
        with Flex(direction="col", gap=5):
            with self._card_wrap("Default Table", "5 rows"):
                with Flex(direction="col", gap=0).className("overflow-x-auto"):
                    Table(
                        headers=["Name","Role","Team","Status","Joined"],
                        rows=[
                            ["Alice Chen",   "Engineer", "Platform", "Active",   "Jan 2023"],
                            ["Bob Martinez", "Designer", "Product",  "Active",   "Mar 2023"],
                            ["Carol White",  "PM",       "Growth",   "Away",     "Jun 2022"],
                            ["Dan Kim",      "Engineer", "Frontend", "Active",   "Sep 2023"],
                            ["Eve Johnson",  "Analyst",  "Data",     "Inactive", "Nov 2022"],
                        ],
                    )
            with self._card_wrap("Striped Table", "striped=True"):
                with Flex(direction="col", gap=0).className("overflow-x-auto"):
                    Table(
                        headers=["Package","Version","License","Downloads"],
                        rows=[
                            ["pyui-framework","0.1.0", "MIT",    "12.4k"],
                            ["click",         "8.1.7", "BSD",    "890M"],
                            ["aiohttp",       "3.9.1", "Apache", "45M"],
                            ["rich",          "13.7.0","MIT",    "120M"],
                            ["watchdog",      "3.0.0", "Apache", "28M"],
                        ],
                    ).striped()

    # =========================================================
    # CHARTS
    # =========================================================
    def _section_charts(self) -> None:
        self._section_header("Charts",
            "Line, Bar, and Pie charts powered by Chart.js.", "charts")
        with Grid(cols=2, gap=5):
            with self._card_wrap("Line Chart", "type=line"):
                with Flex(direction="col", gap=0).className("p-4"):
                    Chart(
                        type="line",
                        labels=["Jan","Feb","Mar","Apr","May","Jun"],
                        datasets=[{
                            "label": "Revenue",
                            "data": [4200,5800,4900,7200,6100,8400],
                            "borderColor": "#111827",
                            "backgroundColor": "rgba(17,24,39,0.06)",
                            "tension": 0.4,
                            "fill": True,
                        }],
                    )
            with self._card_wrap("Bar Chart", "type=bar"):
                with Flex(direction="col", gap=0).className("p-4"):
                    Chart(
                        type="bar",
                        labels=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
                        datasets=[{
                            "label": "Signups",
                            "data": [120,190,150,210,180,90,60],
                            "backgroundColor": "#111827",
                            "borderRadius": 6,
                        }],
                    )
        with Grid(cols=3, gap=5).className("mt-4"):
            with self._card_wrap("Pie Chart", "type=pie"):
                with Flex(direction="col", gap=0).className("p-4"):
                    Chart(
                        type="pie",
                        labels=["Web","Desktop","CLI"],
                        datasets=[{
                            "data": [65,25,10],
                            "backgroundColor": ["#111827","#6b7280","#d1d5db"],
                        }],
                    )
            with self._card_wrap("Multi-Series Line", "2 datasets"):
                with Flex(direction="col", gap=0).className("p-4 col-span-2"):
                    Chart(
                        type="line",
                        labels=["Q1","Q2","Q3","Q4"],
                        datasets=[
                            {
                                "label": "2023",
                                "data": [18000,22000,19500,28000],
                                "borderColor": "#111827",
                                "tension": 0.4,
                            },
                            {
                                "label": "2024",
                                "data": [21000,26000,24000,34000],
                                "borderColor": "#6b7280",
                                "tension": 0.4,
                            },
                        ],
                    )

        # Markdown at the bottom
        with self._card_wrap("Markdown", "marked.js"):
            with self._pad():
                Markdown("""## PyUI Component System

PyUI ships with **42+ production-ready components** organized into six categories:

- **Layout** — `Flex`, `Grid`, `Stack`, `Container`, `Sidebar`, `Split`
- **Display** — `Heading`, `Text`, `Badge`, `Tag`, `Avatar`, `Icon`, `Image`
- **Input** — `Button`, `Input`, `Select`, `Checkbox`, `Toggle`, `Slider`
- **Feedback** — `Alert`, `Toast`, `Modal`, `Drawer`, `Tooltip`, `Progress`
- **Navigation** — `Nav`, `Tabs`, `Breadcrumb`, `Pagination`, `Menu`
- **Data** — `Table`, `Stat`, `Chart`

```python
from pyui import App, Page, Button, Text, reactive

class MyApp(App):
    count = reactive(0)

class Home(Page):
    route = "/"
    def compose(self):
        Text(lambda: f"Count: {MyApp.count.get()}")
        Button("Increment").style("primary").onClick(
            lambda: MyApp.count.set(MyApp.count.get() + 1)
        )
```

> Every component is a Python class. No HTML. No templates. No JavaScript.
""")


class StorybookApp(App):
    name = "PyUI Storybook"
    index = StorybookPage()


def run_storybook(port: int = 8000, open_browser: bool = True) -> None:
    from pyui.server.dev_server import run_dev_server
    run_dev_server(StorybookApp, port=port, open_browser=open_browser)
