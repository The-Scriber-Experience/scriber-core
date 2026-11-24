---
name: tse-visual-styling
description: Scriber Core guide to The Scriber Experience (TSE) visual system, Eigenscribe colors and gradients, plotting themes, CSS tokens, Mermaid styling, and CLI color helpers.
---

### 🖋️ TSE Visual Styling for Scriber Core

Use this skill when styling scientific plots, dashboards, Mermaid diagrams, CSS, or CLI output with The Scriber Experience (TSE), the visual system in the **Eigenscribe** workspace. The PyPI distribution and repository are `scriber-core`; its Python import namespace is `eigenscribe`.

### 🎨 1. Eigenscribe Colors and Gradients

- The single authored Python palette is `COLOR_PALETTE` in `src/eigenscribe/frontend/colors.py`, a flat mapping of token names to six-digit hex values.
- The canonical multi-stop presets are `GRADIENT_PRESETS` in `src/eigenscribe/frontend/gradients.py`. Extend or reuse these instead of copying gradient stop lists. The interpolation engine proportionally spaces keyframes using the Golden Ratio.
- `docs/colors-and-gradients.md` is the human-readable token and preset catalog. Keep new visual code aligned with it and the canonical dictionaries.
- Prefer token keys over repeated hex/RGB literals. Convert hex to RGB with `hex_to_rgb()` when generating ANSI values.

Common palette tokens include:

| Role | Token keys and values |
| :--- | :--- |
| Dark surfaces | `dark_slate` `#0d1117`, `card_black` `#161b22`, `grid_gray` `#21262d` |
| TSE background | `cosmic_center` `#0a0f1f`, `cosmic_void` `#050812`, `pure_black` `#000000` |
| EIGEN spectrum | `node-2` `#00e8ff`, `node-3` `#14b5ff`, `sky_blue` `#3a98ff`, `node-6` `#7952f5` |
| Text and accents | `ice_cyan` `#c8f8ff`, `text_primary` `#f0f6fc`, `success_emerald` `#10b981`, `warning_amber` `#f7c548` |

Use preset names that exist in `GRADIENT_PRESETS`, such as `eigenscribe`, `aurora`, `midnight`, `sunset`, `forest`, and `cyberpunk`. See `docs/colors-and-gradients.md` for the maintained catalog.

### 🐍 2. Python Plotting (Matplotlib, Seaborn, Plotly)

The public plotting helpers are exported from `eigenscribe.frontend` and `eigenscribe.frontend.the_scriber_experience`. Use the Eigenscribe palette and registered TSE theme utilities rather than importing from `boilerplates.python`.

```python
import matplotlib.pyplot as plt
import numpy as np

from eigenscribe.frontend import (
    COLOR_PALETTE,
    GRADIENT_PRESETS,
    apply_cosmic_theme,
    plot_eigenscribe_heatmap,
)

apply_cosmic_theme(seaborn=True)
rng = np.random.default_rng(42)
x = np.linspace(0, 10, 200)
colors = GRADIENT_PRESETS["eigenscribe"]

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(x, np.sin(x), color=COLOR_PALETTE["node-2"], linewidth=2, label="Phase")
ax.plot(x, np.cos(x), color=colors[-1], linewidth=2, label="Carrier")
ax.legend()

matrix = rng.uniform(0, 1, size=(10, 10))
fig_heat, ax_heat = plt.subplots(figsize=(6, 5))
plot_eigenscribe_heatmap(
    matrix,
    style="cosmic_sephirah",
    ax=ax_heat,
    title="TSE Coherence Matrix",
    cbar_label="Intensity",
)
plt.show()
```

`plot_eigenscribe_heatmap()` expects a two-dimensional array. Supported named styles include `cosmic_cyan`, `cosmic_sephirah`, `cosmic_spectrum`, and `cosmic_void_to_cyan`; registered Eigenscribe colormaps can also be used.

For Plotly, use the built-in dark-theme figure factory. Plotly is optional and must be installed separately to call this helper.

```python
from eigenscribe.frontend import create_plotly_base_figure

fig = create_plotly_base_figure("Eigenscribe Phase Dashboard", height=380)
```

### 🌐 3. CSS and Glassmorphism

Follow the four-layer taxonomy in `house-rules/css-rules.md` and use `boilerplates/css/tse-boilerplate.css` as the TSE implementation reference: tokens, resets, layout, then reusable components. Keep existing CSS custom-property names and values consistent with that stylesheet; names such as `--color-bg-cosmic` are established identifiers and should not be renamed casually.

```css
:root {
  --color-bg: #0d1117;
  --color-surface: #161b22;
  --color-bg-cosmic-center: #0a0f1f;
  --color-bg-cosmic: #050812;
  --color-bg-cosmic-void: #000000;
  --gradient-cosmic-radial: radial-gradient(
    circle at center,
    var(--color-bg-cosmic-center) 0%,
    var(--color-bg-cosmic) 60%,
    var(--color-bg-cosmic-void) 100%
  );
  --background-wisp: url("../../assets/images/wisp.jpg");
  --background-wisp-overlay: linear-gradient(rgba(5, 8, 18, 0.72), rgba(5, 8, 18, 0.84));
  --color-text: #f0f6fc;
  --color-text-accent: #c8f8ff;
}

body {
  background-color: var(--color-bg);
  background-image: var(--background-wisp-overlay), var(--background-wisp), var(--gradient-cosmic-radial);
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
  color: var(--color-text);
}
```

Use the stylesheet's spacing, typography, glass, border, and glow tokens for components. Avoid introducing a parallel set of raw colors; when adding a palette color, update the canonical palette and its reference documentation as well.

### 🔱 4. Mermaid and Diagrams

The Mermaid theme helpers live in `eigenscribe.frontend.the_scriber_experience.mermaid`. Reuse their TSE theme variables, class definitions, and directives when generating diagrams so Mermaid output stays consistent with the canonical palette.

### 💻 5. CLI Color Output

CLI styling is implemented in `eigenscribe.cli`, not under `frontend.the_scriber_experience.cli`. TrueColor formatting can use `ansi_color()` with a canonical palette value; `ansi_256()` is available for terminals that require 256-color escapes.

```python
from eigenscribe.cli import ansi_color
from eigenscribe.frontend import COLOR_PALETTE

print(ansi_color(COLOR_PALETTE["node-2"], "Eigenscribe", bold=True))
```

Use the semantic CLI helpers for status messages where appropriate, and do not invent ANSI index mappings for palette tokens. The CLI's color table and gradient commands are generated from the canonical palette and gradient dictionaries.
