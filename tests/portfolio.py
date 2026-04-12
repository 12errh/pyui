from pyui import (
    App,
    Button,
    Container,
    Flex,
    Grid,
    Heading,
    Icon,
    Image,
    Page,
    Stack,
    Text,
)


class PortfolioPage(Page):
    title = "Jacob's Portfolio | Pro Developer"
    route = "/"

    def compose(self) -> None:
        # Full page wrapper with modern typography and strict x-overflow hiding
        with Flex(direction="col").className("min-h-screen w-full bg-[#f8fafc] font-sans text-slate-900 overflow-x-hidden pt-4 lg:pt-8 !max-w-[100vw] selection:bg-orange-500 selection:text-white"):
            
            # --- Navigation ---
            with (
                Container(size="6xl").className("pt-6 pb-4 relative z-50"),
                Flex(justify="between", align="center").className("backdrop-blur-md bg-white/70 px-8 py-4 rounded-full border border-white/20 shadow-[0_8px_30px_rgb(0,0,0,0.04)]"),
            ):
                # Links (Left)
                with Flex(gap=10).className("hidden md:flex text-sm font-bold text-slate-600 uppercase tracking-widest"):
                    Text("About Me").className("hover:text-orange-500 transition-colors cursor-pointer relative after:content-[''] after:absolute after:-bottom-2 after:left-0 after:w-0 after:h-0.5 after:bg-orange-500 after:transition-all hover:after:w-full")
                    Text("Portfolio").className("text-orange-500 cursor-pointer relative after:content-[''] after:absolute after:-bottom-2 after:left-0 after:w-full after:h-0.5 after:bg-orange-500")
                    Text("Testimonial").className("hover:text-orange-500 transition-colors cursor-pointer relative after:content-[''] after:absolute after:-bottom-2 after:left-0 after:w-0 after:h-0.5 after:bg-orange-500 after:transition-all hover:after:w-full")

                # Mobile Menu Icon
                Icon("menu").className("md:hidden text-slate-900 cursor-pointer hover:text-orange-500 transition-colors")

                # Center Logo (The "J" Icon)
                with (
                    Flex(justify="center", align="center").className("absolute left-1/2 -translate-x-1/2 cursor-pointer hover:scale-110 transition-transform duration-500"),
                    Flex(justify="center", align="center").className("w-14 h-14 bg-gradient-to-tr from-slate-900 to-slate-800 text-white rounded-full font-black text-2xl shadow-xl shadow-slate-900/20"),
                ):
                    Text("J")

                # Contact Button
                with Flex().className("hidden md:block"):
                    Button("Contact Me").className("!rounded-full !border-2 !border-slate-200 !bg-transparent !text-slate-900 shadow-sm hover:!border-slate-900 hover:!bg-slate-900 hover:!text-white !px-8 !py-2.5 !text-sm !font-bold uppercase tracking-widest transition-all duration-300")

            # --- Hero Section ---
            with Container(size="6xl").className("relative pt-8 md:pt-12 pb-20"):
                # Decorative background elements
                Flex().className("absolute top-0 right-[20%] w-96 h-96 bg-orange-300/20 rounded-full blur-3xl -z-10 mix-blend-multiply")
                Flex().className("absolute bottom-0 left-[10%] w-72 h-72 bg-blue-300/20 rounded-full blur-3xl -z-10 mix-blend-multiply")

                with Grid(cols=1).className("md:grid-cols-12 gap-12 items-center"):
                    
                    # Hero Typography
                    with (
                        Flex(direction="col").className("md:col-span-6 z-10 space-y-8"),
                        Stack(spacing=5),
                    ):
                        # Small introductory badge
                        with Flex(align="center", gap=2).className("bg-orange-100/50 border border-orange-200 text-orange-600 px-4 py-1.5 rounded-full w-max backdrop-blur-sm"):
                            Icon("sparkles", size=16)
                            Text("Available for freelance work").className("text-sm font-bold tracking-wide")

                            Heading("My name\nis Jacob", level=1).className("text-[5rem] lg:text-[8rem] font-black tracking-tighter whitespace-pre-line leading-[0.9] text-transparent bg-clip-text bg-gradient-to-br from-slate-900 to-slate-700")
                            Text(
                                "I craft high-performance digital experiences\nbridging the gap between design and engineering."
                            ).className("text-slate-500 text-lg lg:text-xl whitespace-pre-line leading-relaxed max-w-lg mt-2 font-medium")
                        
                        with Flex(gap=4, align="center"):
                            Button("Hire Me").className("!bg-gradient-to-r hover:!bg-gradient-to-l !from-[#f97316] !to-[#ea580c] !text-white !rounded-full !px-12 !py-4 w-max font-bold tracking-widest shadow-[0_10px_40px_-10px_rgba(249,115,22,0.8)] transition-all hover:-translate-y-1 hover:shadow-[0_15px_50px_-10px_rgba(249,115,22,0.6)]")
                            
                            with Flex(justify="center", align="center", gap=2).className("h-14 px-6 rounded-full border-2 border-slate-200 cursor-pointer hover:border-slate-400 hover:bg-slate-50 transition-all font-bold text-slate-700 uppercase tracking-widest text-sm"):
                                Text("View Work")

                        # Skill Pills
                        with Flex(direction="col", gap=4).className("pt-4 mt-2"):
                            Text("CORE EXPERTISE").className("text-xs font-black text-slate-400 tracking-widest uppercase")
                            with Flex(wrap=True, gap=3):
                                for skill, icon, color in [("C++", "cpu", "bg-indigo-500"), ("Python", "file-code", "bg-emerald-500"), ("React", "atom", "bg-cyan-500"), ("PyUI", "blocks", "bg-orange-500")]:
                                    with Flex(align="center", gap=2).className("bg-white border border-slate-200 text-slate-700 font-bold px-4 py-2 rounded-full shadow-sm hover:shadow-md hover:-translate-y-1 transition-all cursor-pointer group"):
                                        with Flex(justify="center", align="center").className(f"w-6 h-6 rounded-full {color} text-white"):
                                            Icon(icon, size=12)
                                        Text(skill)

                    # Hero Image and Abstract Shapes
                    with Flex(justify="center").className("md:col-span-6 relative mt-24 md:mt-0 right-0"):
                        # Large abstract orange sweep with gradient
                        Flex().className("absolute left-[10%] top-1/2 -translate-y-1/2 w-[160%] aspect-square bg-gradient-to-br from-orange-400 to-orange-600 rounded-[8rem] rotate-12 -z-10 hidden md:block shadow-2xl opacity-90")
                        Flex().className("absolute inset-0 bg-gradient-to-br from-orange-400 to-orange-600 rounded-full scale-110 -z-10 md:hidden blur-lg opacity-80")
                        
                        with Flex(justify="center").className("relative group"):
                            # The portrait wrapper
                            with Flex(justify="center", align="center").className("w-72 h-72 lg:w-[32rem] lg:h-[32rem] rounded-full overflow-hidden border-[12px] border-white/90 backdrop-blur-xl shadow-[0_20px_60px_-15px_rgba(0,0,0,0.3)] relative z-10 bg-slate-100 transition-all duration-700 group-hover:scale-105 group-hover:rotate-1"):
                                Image("https://images.unsplash.com/photo-1531384441138-2736e62e0919?q=80&w=1000&auto=format&fit=crop").fit("cover").className("w-full h-full object-cover object-top")
                            
                            # Floating Experience Badge - Glassmorphism
                            with Flex(align="center", gap=5).className("absolute bottom-8 -left-8 lg:bottom-16 lg:-left-20 bg-white/10 backdrop-blur-xl border border-white/20 p-6 lg:p-8 rounded-3xl shadow-[0_30px_60px_-15px_rgba(0,0,0,0.5)] z-20 min-w-max transition-transform duration-500 group-hover:-translate-y-4 group-hover:-rotate-3"):
                                with Flex(justify="center", align="center").className("w-16 h-16 rounded-full bg-gradient-to-r from-orange-500 to-orange-400 shadow-lg text-white font-black text-2xl"):
                                    Text("10+")
                                Text("Years of\nExcellence").className("text-sm lg:text-base text-white/90 leading-snug tracking-wider uppercase font-extrabold whitespace-pre-line")

            # --- Client Marquee ---
            with Flex(justify="around", align="center", wrap=True, gap=10).className("py-16 border-y border-slate-200/50 bg-gradient-to-r from-white via-slate-50 to-white"):
                for client in ["acme corp", "globex", "soylent", "initech", "umbrella"]:
                    Text(client).className("text-3xl font-black text-slate-300 uppercase tracking-widest hover:text-slate-800 transition-colors duration-500 cursor-pointer")

            # --- Services ---
            with Container(size="6xl").className("py-32 relative"):
                # Decorative background text
                Text("SERVICES").className("absolute top-20 left-0 text-[12rem] font-black text-slate-100 -z-10 leading-none select-none tracking-tighter")

                with (
                    Flex(justify="between", align="end").className("mb-20"),
                    Stack(spacing=4),
                    Flex(align="center", gap=3),
                ):
                    Flex().className("w-8 h-1 bg-orange-500 rounded-full")
                    Text("What I Do").className("text-orange-500 font-black tracking-widest uppercase text-sm")
                    Heading("Expertise Area", level=2).className("text-5xl lg:text-7xl font-black tracking-tighter text-slate-900")
                        
                with Grid(cols=1).className("md:grid-cols-3 gap-8"):
                    # Service 1
                    with Flex(direction="col", justify="center", align="start").className("bg-white p-10 lg:p-12 rounded-[2.5rem] shadow-[0_10px_40px_-20px_rgba(0,0,0,0.1)] border border-slate-100 hover:shadow-[0_20px_50px_-20px_rgba(0,0,0,0.2)] hover:-translate-y-3 transition-all duration-500 group cursor-pointer relative overflow-hidden"):
                        Flex().className("absolute top-0 right-0 w-32 h-32 bg-orange-500/10 rounded-bl-[100px] -z-10 transition-transform duration-500 group-hover:scale-150")
                        with Flex(justify="center", align="center").className("w-20 h-20 rounded-3xl bg-orange-50 text-orange-500 mb-8 group-hover:bg-gradient-to-br group-hover:from-orange-400 group-hover:to-orange-600 group-hover:text-white transition-all duration-500 shadow-sm"):
                            Icon("layout", size=32)
                        Heading("UI/UX Design", level=3).className("text-3xl font-black mb-4 tracking-tight")
                        Text("Crafting pixel-perfect interface experiences that convert users and delight clients with modern aesthetics.").className("text-slate-500 leading-relaxed font-medium")
                        with Flex(align="center", gap=2).className("mt-8 text-orange-500 font-bold uppercase tracking-widest text-sm group-hover:text-orange-600 transition-colors"):
                            Text("Learn More")
                            Icon("arrow-right", size=16).className("group-hover:translate-x-2 transition-transform")
                    
                    # Service 2 - Highlighted Dark Mode Card
                    with Flex(direction="col", justify="center", align="start").className("bg-gradient-to-br from-slate-900 to-slate-800 p-10 lg:p-12 rounded-[2.5rem] shadow-[0_20px_50px_-15px_rgba(0,0,0,0.5)] hover:shadow-[0_30px_60px_-15px_rgba(0,0,0,0.6)] hover:-translate-y-3 transition-all duration-500 group cursor-pointer relative overflow-hidden"):
                        Flex().className("absolute top-0 right-0 w-32 h-32 bg-white/5 rounded-bl-[100px] -z-10 transition-transform duration-500 group-hover:scale-150")
                        with Flex(justify="center", align="center").className("w-20 h-20 rounded-3xl bg-white/10 text-white mb-8 group-hover:bg-gradient-to-br group-hover:from-orange-400 group-hover:to-orange-600 transition-all duration-500 shadow-sm backdrop-blur-md"):
                            Icon("code-2", size=32)
                        Heading("Web Dev", level=3).className("text-3xl font-black mb-4 tracking-tight text-white")
                        Text("Building robust full-stack applications with modern frameworks, focusing on performance and scalability.").className("text-slate-300 leading-relaxed font-medium")
                        with Flex(align="center", gap=2).className("mt-8 text-white font-bold uppercase tracking-widest text-sm opacity-80 group-hover:opacity-100 transition-opacity"):
                            Text("Learn More")
                            Icon("arrow-right", size=16).className("group-hover:translate-x-2 transition-transform")

                    # Service 3
                    with Flex(direction="col", justify="center", align="start").className("bg-white p-10 lg:p-12 rounded-[2.5rem] shadow-[0_10px_40px_-20px_rgba(0,0,0,0.1)] border border-slate-100 hover:shadow-[0_20px_50px_-20px_rgba(0,0,0,0.2)] hover:-translate-y-3 transition-all duration-500 group cursor-pointer relative overflow-hidden"):
                        Flex().className("absolute top-0 right-0 w-32 h-32 bg-orange-500/10 rounded-bl-[100px] -z-10 transition-transform duration-500 group-hover:scale-150")
                        with Flex(justify="center", align="center").className("w-20 h-20 rounded-3xl bg-orange-50 text-orange-500 mb-8 group-hover:bg-gradient-to-br group-hover:from-orange-400 group-hover:to-orange-600 group-hover:text-white transition-all duration-500 shadow-sm"):
                            Icon("smartphone", size=32)
                        Heading("App Design", level=3).className("text-3xl font-black mb-4 tracking-tight")
                        Text("Designing intuitive, native micro-interactions for iOS and Android platforms to maximize engagement.").className("text-slate-500 leading-relaxed font-medium")
                        with Flex(align="center", gap=2).className("mt-8 text-orange-500 font-bold uppercase tracking-widest text-sm group-hover:text-orange-600 transition-colors"):
                            Text("Learn More")
                            Icon("arrow-right", size=16).className("group-hover:translate-x-2 transition-transform")


            # --- Latest Projects ---
            with Flex().className("w-full py-32 bg-slate-900 rounded-[4rem] text-white my-10 relative overflow-hidden"):
                # Decorative dark grid pattern (simulated)
                Flex().className("absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-slate-800 to-slate-900 -z-10")
                
                with Container(size="6xl").className("w-full relative z-10"):
                    # Section Header
                    with Flex(justify="between", align="end").className("mb-24"):
                        with Stack(spacing=4):
                            with Flex(align="center", gap=3):
                                Flex().className("w-8 h-1 bg-orange-500 rounded-full")
                                Text("Portfolio").className("text-orange-500 font-black tracking-widest uppercase text-sm")
                            Heading("Featured Works", level=2).className("text-5xl lg:text-7xl font-black tracking-tighter text-white")
                        
                        with Flex(align="center", gap=4).className("cursor-pointer group"):
                            Text("All projects").className("text-sm font-bold uppercase tracking-widest text-slate-300 group-hover:text-white transition-colors")
                            with Flex(justify="center", align="center").className("w-14 h-14 rounded-full bg-white/10 text-white group-hover:bg-orange-500 group-hover:scale-110 transition-all duration-300"):
                                Icon("arrow-up-right", size=24)

                    # Projects Grid
                    with Grid(cols=1).className("sm:grid-cols-2 lg:grid-cols-3 gap-10"):
                        
                        # Project 1: Space Age 90
                        with Stack(spacing=6).className("group cursor-pointer"):
                            with Flex(justify="center", align="center").className("w-full aspect-[4/3] bg-gradient-to-br from-[#2a2a2a] to-[#1a1a1a] rounded-[2rem] relative overflow-hidden"):
                                with Flex(justify="center", align="center").className("absolute inset-6 rounded-xl overflow-hidden shadow-2xl"):
                                    Image("https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=800&auto=format&fit=crop").fit("cover").className("w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 ease-out")
                                    # Dark hover overlay
                                    Flex().className("absolute inset-0 bg-slate-900/0 group-hover:bg-slate-900/20 transition-colors duration-500")
                                with Flex(justify="center", align="center").className("absolute bottom-8 right-8 w-16 h-16 bg-white text-slate-900 rounded-2xl shadow-xl z-20 group-hover:bg-orange-500 group-hover:text-white transition-colors duration-300"):
                                    Icon("arrow-up-right", size=28)
                            with Flex(direction="col", gap=2).className("px-2"):
                                Text("Space Age 90").className("font-black text-3xl group-hover:text-orange-400 transition-colors tracking-tight")
                                Text("Digital Art Direction").className("text-sm text-slate-400 font-bold tracking-widest uppercase")

                        # Project 2: AMC for App
                        with Stack(spacing=6).className("group cursor-pointer lg:-translate-y-12"): # Staggered layout
                            with Flex(justify="center", align="center").className("w-full aspect-[4/3] bg-gradient-to-br from-[#fcd4b8] to-[#f3b58c] rounded-[2rem] relative overflow-hidden"):
                                Heading("AMC", level=3).className("text-7xl font-black tracking-tighter text-[#4a2e1b] group-hover:scale-110 transition-transform duration-700 ease-out")
                                Flex().className("absolute inset-0 bg-black/0 group-hover:bg-black/5 transition-colors duration-500")
                                with Flex(justify="center", align="center").className("absolute bottom-8 right-8 w-16 h-16 bg-white text-slate-900 rounded-2xl shadow-xl z-20 group-hover:bg-orange-500 group-hover:text-white transition-colors duration-300"):
                                    Icon("arrow-up-right", size=28)
                            with Flex(direction="col", gap=2).className("px-2"):
                                Text("AMC for App").className("font-black text-3xl group-hover:text-orange-400 transition-colors tracking-tight")
                                Text("UI & Branding").className("text-sm text-slate-400 font-bold tracking-widest uppercase")

                        # Project 3: Doremius
                        with Stack(spacing=6).className("group cursor-pointer"):
                            with Flex(justify="center", align="center").className("w-full aspect-[4/3] bg-white border border-slate-800 rounded-[2rem] relative overflow-hidden"):
                                with Flex(justify="center", align="center").className("absolute inset-6 rounded-xl overflow-hidden shadow-2xl"):
                                    Image("https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?q=80&w=800&auto=format&fit=crop").fit("cover").className("w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 ease-out")
                                    Flex().className("absolute inset-0 bg-slate-900/0 group-hover:bg-slate-900/20 transition-colors duration-500")
                                with Flex(justify="center", align="center").className("absolute bottom-8 right-8 w-16 h-16 bg-slate-900 text-white rounded-2xl shadow-xl z-20 group-hover:bg-orange-500 transition-colors duration-300"):
                                    Icon("arrow-up-right", size=28)
                            with Flex(direction="col", gap=2).className("px-2"):
                                Text("Doremius").className("font-black text-3xl group-hover:text-orange-400 transition-colors tracking-tight")
                                Text("Mobile Application").className("text-sm text-slate-400 font-bold tracking-widest uppercase")

            # --- Testimonial ---
            with Container(size="4xl").className("py-40 text-center relative"):
                Icon("quote", size=120, color="#f97316").className("absolute top-20 left-1/2 -translate-x-1/2 opacity-[0.03]")
                
                with Flex(direction="col", align="center", gap=12).className("relative z-10"):
                    with Flex(gap=1).className("text-orange-500"):
                        for _ in range(5):
                            Icon("star", size=24, color="#f97316")
                            
                    Heading("Jacob delivered an exceptional digital experience. His profound understanding of modern aesthetics and flawless technical execution transformed our brand entirely.", level=2).className("text-3xl lg:text-5xl font-bold tracking-tight text-slate-800 leading-tight")
                    
                    with Flex(align="center", gap=6).className("bg-white py-4 px-8 rounded-full shadow-[0_10px_40px_-15px_rgba(0,0,0,0.1)] border border-slate-100"):
                        with Flex(justify="center", align="center").className("w-16 h-16 rounded-full border-2 border-slate-100 shadow-md overflow-hidden"):
                            Image("https://images.unsplash.com/photo-1494790108377-be9c29b29330?q=80&w=150&auto=format&fit=crop").fit("cover").className("w-full h-full object-cover")
                        with Flex(direction="col", align="start", gap=1):
                            Text("Sarah Jenkins").className("font-black text-xl text-slate-900")
                            Text("CEO at Acme Corp").className("text-xs font-bold text-orange-500 uppercase tracking-widest")

            # --- Footer / CTA ---
            with Flex().className("w-full bg-gradient-to-b from-orange-500 to-orange-600 text-white py-32 lg:py-40 mt-10 rounded-t-[4rem] relative overflow-hidden"):
                # Decorative background text
                Text("LET'S TALK").className("absolute -top-12 -right-20 text-[25rem] font-black text-white opacity-5 tracking-tighter leading-none select-none blur-sm")
                
                with Container(size="6xl").className("relative z-10"):
                    with (
                        Grid(cols=1).className("md:grid-cols-2 gap-20 items-center"),
                        Stack(spacing=10),
                    ):
                        Heading("Have an idea?\nLet's build it.", level=2).className("text-6xl lg:text-[5.5rem] font-black tracking-tighter leading-[1.05] !text-white whitespace-pre-line drop-shadow-lg")
                        Text("I'm currently available for freelance projects. Let's create something extraordinary together.").className("text-orange-100 text-xl lg:text-2xl max-w-lg font-medium")
                        
                        with Flex(align="center", gap=6).className("mt-4"):
                            Button("Start a Project").className("!bg-slate-900 hover:!bg-white hover:!text-slate-900 !text-white !rounded-full !px-12 !py-5 w-max font-black uppercase tracking-widest shadow-2xl transition-all hover:-translate-y-1 hover:shadow-white/20")
                            with Flex(justify="center", align="center", gap=3).className("group cursor-pointer"):
                                with Flex(justify="center", align="center").className("w-14 h-14 rounded-full border-2 border-white/30 group-hover:border-white group-hover:bg-white group-hover:text-orange-500 transition-all"):
                                    Icon("play", size=20)
                                Text("Watch Showreel").className("font-bold tracking-widest uppercase text-sm group-hover:translate-x-1 transition-transform")

                    with Flex(direction="col", gap=14, align="end").className("md:text-right relative z-10 w-full"):
                            with Flex(direction="col", gap=3, align="end").className("group cursor-pointer"):
                                Text("Drop a line").className("text-orange-200 text-sm uppercase tracking-widest font-black !block")
                                Text("hello@jacob.dev").className("text-3xl lg:text-4xl font-black group-hover:text-slate-900 transition-colors duration-300 !block underline decoration-white/30 decoration-2 underline-offset-8 group-hover:decoration-slate-900")
                            
                            with Flex(direction="col", gap=3, align="end").className("group cursor-pointer"):
                                Text("Give a ring").className("text-orange-200 text-sm uppercase tracking-widest font-black !block")
                                Text("+1 (555) 123-4567").className("text-3xl lg:text-4xl font-black group-hover:text-slate-900 transition-colors duration-300 !block")

                            with Flex(gap=6):
                                for social in ["twitter", "linkedin", "github", "dribbble", "instagram"]:
                                    with Flex(justify="center", align="center").className("w-16 h-16 rounded-full bg-white/10 border border-white/20 hover:bg-slate-900 hover:border-slate-900 hover:-translate-y-2 transition-all duration-300 cursor-pointer shadow-lg backdrop-blur-sm group"):
                                        Icon(social, size=24, color="#ffffff").className("group-hover:scale-110 transition-transform")

            # Copyright Strip
            with Flex(justify="between", align="center", wrap=True, gap=6).className("w-full bg-slate-950 py-8 px-8 lg:px-20"):
                Text("© 2026 JACOB DEVELOPER. ALL RIGHTS RESERVED.").className("text-xs font-black text-slate-500 uppercase tracking-widest")
                with Flex(gap=8):
                    for link in ["Privacy Policy", "Terms of Service", "Cookies"]:
                        Text(link).className("text-xs font-bold text-slate-500 uppercase tracking-widest hover:text-white transition-colors cursor-pointer")

class PortfolioApp(App):
    name = "Jacob Portfolio"
    index = PortfolioPage()

if __name__ == "__main__":
    from pyui.server.dev_server import run_dev_server
    run_dev_server(PortfolioApp, port=9010)
