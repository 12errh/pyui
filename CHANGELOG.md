# Changelog

All notable changes to PyUI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-04-12

### Added
- **Phase 1: Core Layout & Foundational Components**
  - Foundational components: `Button`, `Text`, `Heading`
  - Core layouts: `Flex`, `Stack`, `Grid`, `Container`
  - Named slots for layouts (e.g. `Sidebar`, `Split`)
  - Initial `WebGenerator` with Tailwind CSS integration
- **Phase 2: Full Component Library & CLI enhancements**
  - **42 New Components**:
    - Layout: `Divider`, `Spacer`, `Sidebar`, `Split`
    - Display: `Badge`, `Tag`, `Avatar`, `Icon` (Lucide), `Image`, `Markdown` (Marked.js), `Video`
    - Inputs: `Input`, `Textarea`, `Select`, `Checkbox`, `Radio`, `Toggle`, `Slider`, `DatePicker`, `FilePicker`, `Form`
    - Feedback: `Alert`, `Toast`, `Modal`, `Drawer`, `Tooltip`, `Progress`, `Spinner`, `Skeleton`
    - Navigation: `Nav`, `Tabs`, `Breadcrumb`, `Pagination`, `Menu`
    - Data Viz: `Table`, `Stat`, `Chart` (Line, Bar, Pie via Chart.js)
  - **CLI Tools**: Added `pyui storybook` command to launch the component gallery
  - **Architecture**: Implemented `compose()` method on Pages and `BaseComponent` context manager for declarative UI building
  - **Renderer**: Full Alpine.js integration for interactive components (Modals, Charts, Tabs)

### Fixed
- Resolved `AttributeError` for missing `__version__` in root package
- Fixed `ImportError` for missing component exports in `src/pyui/__init__.py`
- Corrected `Page` and `Heading` constructor patterns to support declarative use

## [0.0.1] - 2026-04-10

### Added
- Phase 0: Project setup and foundations
  - `pyproject.toml` with hatchling build system
  - `App` and `Page` base classes
  - `BaseComponent` with full chainable API
  - `ReactiveVar` state system
  - GitHub Actions & pre-commit hooks
