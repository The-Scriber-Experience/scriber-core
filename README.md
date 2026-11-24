# 🧿 Scriber Labs: Agent Workspace Index

[![Publish to PyPI](https://github.com/The-Scriber-Experience/scriber-core/actions/workflows/publish.yml/badge.svg)](https://github.com/The-Scriber-Experience/scriber-core/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/scriber-core.svg)](https://pypi.org/project/scriber-core/)
[![Python versions](https://img.shields.io/pypi/pyversions/scriber-core.svg)](https://pypi.org/project/scriber-core/)

Welcome to the canonical environment index for autonomous development agents. This workspace enforces strict structural layout layering, deterministic mathematical simulation profiling, uncompromising code verification rules, and automated workspace consistency.

## 🧭 System Onboarding Directory

```text
├── docs/
│   ├── workspace-setup-guide.md        # Multi-project distribution & setup guide (Submodules / Templates / Packaging)
│   └── COOP_blog/                      # Reference archive of CERFACS COOP software standards
├── house-rules/
│   ├── python-rules.md               # Mathematical typography, packaging hygiene & consistency rules
│   └── css-rules.md                  # Glassmorphic visual layout layering standards
├── boilerplates/
│   ├── css/
│   │   └── tse-boilerplate.css         # Eigenscribe signature high-contrast layout blueprint
│   ├── mermaid/
│   │   └── boilerplate_diagram.mmd     # Dark-mode Mermaid diagram architecture template
│   ├── notebooks/
│   │   └── visuals-boilerplate.ipynb   # Visualizations, NetworkX topologies & color palettes template
│   └── python/
│       ├── gold-standard.py            # Gold standard numeric integration template
│       └── visualization_boilerplate.py # Matplotlib, Seaborn & Plotly theme bootstrap template
├── src/
│   └── eigenscribe/                  # 📦 Single top-level package (frontend + cli subpackages)
│       ├── __init__.py               # Exports __version__; re-exports frontend & cli subpackages
│       ├── __main__.py                # Primary package launcher (`python -m eigenscribe`)
│       ├── cli/                      # 💻 Primary Scriber Core CLI suite & TrueColor tools
│       │   ├── __init__.py           # CLI package exports & public API
│       │   ├── __main__.py           # Package execution entry point (`python -m eigenscribe.cli`)
│       │   ├── main.py               # Command router, gradient banners, and command catalog
│       │   ├── messaging.py          # Semantic status alerts, ANSI 256 palette & banner generator
│       │   └── colors_table.py       # COLOR_PALETTE table renderer with TrueColor swatches
│       └── frontend/                 # 🎨 Frontend, design tokens & styling subsystem
│           ├── __init__.py
│           ├── colors.py             # Canonical palette (COLOR_PALETTE), semantic/CLI/EIGEN roles, RGB, hex_to_rgb
│           ├── gradients.py          # Golden ratio TrueColor multi-stop gradient engine (GRADIENT_PRESETS)
│           └── the_scriber_experience/   # 🔱 The Scriber Experience (TSE) styling subsystems
│               ├── __init__.py
│               ├── plots/            # Scientific plotting themes & colormaps
│               │   ├── __init__.py
│               │   └── theme.py      # Theme engine for Matplotlib, Pyplot, Seaborn, Plotly
│               └── mermaid/          # Dark-mode Mermaid.js diagram theme engine & preview
│                   ├── __init__.py
│                   └── theme.py      # Class definitions, directives & HTML preview renderer
├── sublime-theme/
│   ├── EigenScribe/                  # Sublime Text 4 package (theme, color scheme, PreTeXt syntax & snippets)
│   ├── install.sh                    # Bash installer (macOS / Linux, copy or symlink mode)
│   ├── install.ps1                   # PowerShell installer (Windows)
│   └── README.md                     # Package documentation, installation, and configuration guide
├── .junie/
│   ├── AGENTS.md                     # Canonical agent guidelines & workspace directives
│   └── skills/
│       └── tse-visual-styling/       # Workspace skill for The Scriber Experience (TSE) visual system
├── pyproject.toml                    # PyPI packaging & uv dependency configuration (v2.0.1)
└── README.md                         # Master onboarding index (This file)
```

## 🛠️ Infrastructure & Tooling Lock-ins

- **Package & Environment Manager**: `uv` (Deterministic synchronization via `uv sync`).
- **Target Runtime Engine**: Python 3.11+
- **Primary IDE Workspace**: JetBrains PyCharm Professional / IntelliJ IDEA.

## 💻 Eigenscribe CLI Suite (`eigenscribe`)

`scriber-core` provides a unified, color-coded CLI suite in `src/eigenscribe/cli/` featuring signature TrueColor gradient banners, golden ratio-proportioned gradient text, interactive palette tables, and structured command catalogs. The `eigenscribe` console command is the primary interface; the package can also be run with `python -m eigenscribe` or `python -m eigenscribe.cli`:

```bash
# Sync dependencies and development tools
uv sync --extra dev

# Run default CLI entry point (prints SECONDARY_GRADIENT banner & color-coded command catalog)
uv run eigenscribe

# Display the high-contrast ADHD-optimized command catalog
uv run eigenscribe commands

# Render the signature TrueColor block text banner (or custom text)
uv run eigenscribe banner "SCRIBER-CORE"

# Inspect the canonical COLOR_PALETTE with TrueColor swatch blocks, hex, RGB, and ANSI escapes
uv run eigenscribe colors-table
uv run python -m eigenscribe.cli.colors_table --block-width 6 --sort hue

# Render TrueColor multi-stop gradients with Golden Ratio keyframe scaling
uv run eigenscribe gradient "Deterministic Autonomous Agent Baseline" --preset eigenscribe
uv run eigenscribe gradient "Northern Lights" --preset aurora

# Display architecture telemetry, active token counts, and gradient presets
uv run eigenscribe info

# Run built-in self-diagnostics and CLI smoke tests
uv run eigenscribe smoke-test
```

CLI colors are emitted as ANSI TrueColor (24-bit RGB). Use a modern terminal with ANSI/TrueColor support; on Windows, the CLI enables virtual-terminal processing when it can access a console handle. Click 8.5 or newer is required to avoid older Windows ANSI conversion corrupting RGB color sequences. In Git Bash/UCRT64, sync and activate this checkout before using the bare `eigenscribe` command shown in the terminal:

```bash
uv sync --extra dev
source .venv/Scripts/activate
eigenscribe
```

Alternatively, run `uv run eigenscribe` without activating the environment. Windows MSYS pipe output is configured as UTF-8 unless `PYTHONIOENCODING` is explicitly set. If you installed an editable copy into a separate environment, activate that same environment and run `uv pip install --editable .`; an `eigenscribe` executable elsewhere on `PATH` may still use its own older Click installation. The CLI warns when it detects Click older than 8.5 in an MSYS terminal. Redirected output to ordinary files is left unchanged by Windows console setup. In PyCharm, enable terminal emulation for the Run output console; other terminal emulators or IDE consoles that do not support TrueColor may show limited or no color.

### 🎯 Cognitive Load & ADHD Semantic Color Coding

The command directory and CLI outputs implement an ergonomic visual hierarchy to eliminate reading fatigue and accelerate command scanning:
- **`PRIMARY_GRADIENT`**: The `eigenscribe` preset for section headers and diagnostic headings, interpolated with Golden Ratio decay ($\phi \approx 1.618$).
- **`SECONDARY_GRADIENT`**: The `purple_gradient` preset for banners, subtitles, and decorative framing.
- **Palette tokens**: CLI names, syntax, descriptions, borders, and status badges reference `COLOR_PALETTE` keys such as `node-2`, `pale_lilac`, `ice_blue`, and `success_emerald`.

---

## 🎨 Repo-Wide Hex Color Standard & Design Token Architecture

To ensure strict visual fidelity across CLI TrueColor output, Matplotlib/Seaborn plotting themes, dark-mode Mermaid diagrams, and CSS tokens, `scriber-core` enforces a mandatory repo-wide color standard:

1. **Single Source of Truth (`COLOR_PALETTE`)**:
   - `COLOR_PALETTE` in `src/eigenscribe/frontend/colors.py` owns all authored hex tokens. Gradients, CLI styling, and plotting themes reference these canonical values instead of defining parallel hex dictionaries.
2. **Repo-Wide Hex Constraint**:
   - **Color variables reference valid `COLOR_PALETTE` token keys; direct hex values are reserved for the canonical palette and caller-supplied custom colors.**
   - Convert palette colors with `hex_to_rgb()` rather than repeating RGB constants in downstream modules.
3. **Deterministic RGB Normalization**:
   - The `hex_to_rgb(hex_code)` utility in `src/eigenscribe/frontend/colors.py` provides deterministic conversion from hex strings to `(R, G, B)` integer tuples for ANSI escape sequence generation (`\033[38;2;R;G;Bm`).
4. **Golden Ratio Multi-Stop Gradient Interpolation**:
   - Multi-stop gradients computed via `multi_gradient()` scale keyframe segment lengths according to the Golden Ratio ($\phi \approx 1.618$, $w_k = (1/\phi)^k$).
   - Segments taper smoothly from dominant blues and cyans on the left to violets, purples, and magentas on the right.

---

## 🔱 Additional Eigenscribe CLI Commands (`eigenscribe`)

The `eigenscribe` console script also provides design-token inspection and diagnostics:

```bash
# Run design system diagnostics & theme exports
uv run eigenscribe doctor
uv run eigenscribe theme --format css
uv run eigenscribe mermaid --sample
```

## 📦 Cross-Project Distribution & Package Setup

`scriber-core` serves as the single source of truth across all **Eigenscribe Inc.** and **Scriber Labs** projects. There are three core ways to utilize and package this workspace:

1. **Git Submodule (Existing Projects)**:
   - Link this workspace into target repositories:
     ```bash
     git submodule add <SCRIBER_CORE_REPO_URL> .scriber-core
     ```
   - Connect guidelines via `.junie/AGENTS.md` bridging to `.scriber-core/house-rules/...`.
   - Update anytime with: `git submodule update --remote --merge`.

2. **Template Repository (Green-field Projects)**:
   - Enable template mode in repository settings and click **"Use this template"**.
   - Cloned projects inherit the canonical directory structure (`house-rules/`, `boilerplates/`, `.junie/AGENTS.md`).

3. **Installable Python Package Configuration (`src/` Layout)**:
   - To configure consumer projects as installable Python libraries using `uv`:
     - Adopt standard layout: `src/<package_name>/__init__.py` and `src/<package_name>/core.py`.
     - Configure `pyproject.toml` with `[build-system]` (`hatchling`) and `[tool.uv]` (`package = true`).
     - Install and sync in editable mode with `uv sync` or `uv pip install -e .`.

### 🚀 Automated PyPI Release & Consumption

Releases are published automatically by the [`.github/workflows/publish.yml`](.github/workflows/publish.yml) GitHub Actions workflow, which tests (Python 3.10–3.12), builds with `uv build`, and uploads to PyPI via **Trusted Publishing (OIDC — no stored tokens)** whenever a `vX.Y.Z` SemVer tag is pushed. Manual `workflow_dispatch` runs can also target TestPyPI. See `docs/workspace-setup-guide.md` (Section 11) for the release protocol and the one-time PyPI Trusted Publisher setup.

Once published, bootstrap any other project with the shared workspace, CLI, and styling tokens:

```bash
# Add as a dependency (uv) or install directly (pip)
uv add scriber-core          # or: pip install scriber-core

# Use the bundled CLI...
eigenscribe --help

# ...and import the canonical design tokens from your own code
python -c "from eigenscribe.frontend import COLOR_PALETTE, GRADIENT_PRESETS; print(len(COLOR_PALETTE))"
```

### Import namespace migration

The Python import namespace is now `eigenscribe`; update imports such as `from scriber_core.frontend import ...` to `from eigenscribe.frontend import ...`. This is a breaking import change for existing consumers. The installed distribution remains `scriber-core`, and the CLI remains `eigenscribe`.

For detailed, step-by-step walkthroughs, see [`docs/workspace-setup-guide.md`](docs/workspace-setup-guide.md).

## 🎛️ Agent Execution House Rules & End-of-Run Consistency

Before executing any generation loop, training pass, or asset construction, agents must ingest and strictly conform to the sub-system specifications:

1. **Python Rules (`/house-rules/python-rules.md`)**: Forces explicit LaTeX/text derivations, checks array dimensionality boundaries to eliminate silent broadcasting traps, binds modern `np.random.default_rng()` constraints, and mandates explicit `__all__` exports.
2. **CSS Rules (`/house-rules/css-rules.md`)**: Dictates strict, predictable flex/grid container scaffolds using the Eigenscribe high-contrast token spectrum.
3. **End-of-Run File Consistency & Hygiene**:
   - For palette or gradient changes, follow the targeted maintenance matrix in [`.junie/AGENTS.md`](.junie/AGENTS.md) and update direct consumers only; dynamic CLI views derive from the canonical dictionaries.
   - For other changes, verify the affected configuration, documentation, public exports, and tests rather than sweeping unrelated files.
   - No orphan, out-of-sync, or undocumented artifacts may remain at the end of a run.

For each repository, establish:

- What the project actually does.
- What has been implemented and tested.
- What the figures and results genuinely demonstrate.
- What remains speculative or unfinished.
- Where the relevant mathematical reasoning lives.

## 🏛️ Standards & References

Packaging, versioning, branching, CLI architecture, and scientific parameter validation standards are synthesized from modern PEP 517/518/621 declarative tooling (`uv`, `hatchling`) and the CERFACS COOP software engineering standards:

- **COOP Gold Standard**: Dauptain, Antoine. *"Python packages: the COOP gold standard"*, The COOP Blog, CERFACS (Feb 21, 2022). [Web](https://cerfacs.fr/coop/coop-standard-on-python-pkges) | Local: [`docs/COOP_blog/Python packages_ the COOP gold standard · The COOP Blog.html`](docs/COOP_blog/Python%20packages_%20the%20COOP%20gold%C2%A0standard%20%C2%B7%20The%20COOP%20Blog.html)
- **COOP Packaging Guide**: *"Packaging guide"*, The COOP Blog, CERFACS. [Web](https://cerfacs.fr/coop/packaging-guide) | Local: [`docs/COOP_blog/Packaging guide · The COOP Blog.html`](docs/COOP_blog/Packaging%C2%A0guide%20%C2%B7%20The%20COOP%20Blog.html)
- **COOP Click CLI Architecture**: *"The COOP Click Command line interfaces"*, The COOP Blog, CERFACS. [Web](https://cerfacs.fr/coop/the-coop-click-command-line-interfaces) | Local: [`docs/COOP_blog/The COOP Click Command line interfaces · The COOP Blog.html`](docs/COOP_blog/The%20COOP%20Click%20Command%20line%C2%A0interfaces%20%C2%B7%20The%20COOP%20Blog.html)
- **COOP Cactus Branching Model**: *"The Coop Cactus branching model"*, The COOP Blog, CERFACS. [Web](https://cerfacs.fr/coop/the-coop-cactus-branching-model) | Local: [`docs/COOP_blog/The Coop Cactus branching model · The COOP Blog.html`](docs/COOP_blog/The%20Coop%20Cactus%20branching%C2%A0model%20%C2%B7%20The%20COOP%20Blog.html)
- **JSON Schema for Scientific Applications**: *"Using the json-SCHEMA standard for scientific applications"*, The COOP Blog, CERFACS. [Web](https://cerfacs.fr/coop/using-the-json-schema-standard-for-scientific-applications) | Local: [`docs/COOP_blog/Using the json-SCHEMA standard for scientific applications_ · The COOP Blog.html`](docs/COOP_blog/Using%20the%20json-SCHEMA%20standard%20for%20scientific%C2%A0applications_%20%C2%B7%20The%20COOP%20Blog.html)

For exhaustive architecture specifications and step-by-step guides, consult [`docs/workspace-setup-guide.md`](docs/workspace-setup-guide.md).

---
🔬 *Eigenscribe Inc. 2025-2026. Part of the Scriber Labs Research Framework.*
