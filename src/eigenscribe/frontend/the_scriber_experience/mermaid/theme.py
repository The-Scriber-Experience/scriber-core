# src/eigenscribe/frontend/the_scriber_experience/mermaid/theme.py
"""
theme.py

Eigenscribe Mermaid Diagram Theme Generator & Styling Engine.
Provides dark-mode-first Mermaid.js theme configurations, custom class definitions,
diagram wrapping, and HTML preview rendering conforming to The Scriber Experience design system.

Author: Eigenscribe & Scriber Labs
Date: November 15, 2026
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Final, TypeAlias

from eigenscribe.frontend.colors import COLOR_PALETTE, Color, RGB, hex_to_rgb

__all__: list[str] = [
    "EIGENSCRIBE_MERMAID_THEME_VARIABLES",
    "EIGENSCRIBE_MERMAID_CLASSES",
    "get_mermaid_theme_variables",
    "get_mermaid_init_directive",
    "get_mermaid_class_defs",
    "wrap_mermaid_diagram",
    "generate_mermaid_flowchart",
    "render_html_preview",
    "save_mermaid_diagram",
]

# -----------------------------------------------------------------------------------------------------------
# 0️⃣ / 🎭 Definitions, Constants & Types
# -----------------------------------------------------------------------------------------------------------

ThemeDict: TypeAlias = dict[str, Any]


def _rgba(token: str, alpha: float) -> str:
    """Build an RGBA string from a canonical palette token."""
    red, green, blue = hex_to_rgb(COLOR_PALETTE[token])
    return f"rgba({red}, {green}, {blue}, {alpha:g})"


# Foundation Eigenscribe Dark Surface Tokens
SURFACE_BG: Final[str] = COLOR_PALETTE["dark_slate"]
SURFACE_CARD: Final[str] = COLOR_PALETTE["card_black"]
SURFACE_ELEVATED: Final[str] = COLOR_PALETTE["grid_gray"]
BORDER_DEFAULT: Final[str] = COLOR_PALETTE["border_gray"]
BORDER_CYAN_GLOW: Final[str] = COLOR_PALETTE["node-2"]
TEXT_PRIMARY: Final[str] = COLOR_PALETTE["text_primary"]
TEXT_MUTED: Final[str] = COLOR_PALETTE["text_muted"]
TEXT_ACCENT: Final[str] = COLOR_PALETTE["ice_cyan"]

# Default Eigenscribe Mermaid Theme Variables
EIGENSCRIBE_MERMAID_THEME_VARIABLES: Final[dict[str, str]] = {
    # Foundation
    "darkMode": "true",
    "background": SURFACE_BG,
    "primaryColor": SURFACE_CARD,
    "primaryTextColor": TEXT_PRIMARY,
    "primaryBorderColor": BORDER_CYAN_GLOW,
    "lineColor": BORDER_CYAN_GLOW,
    "secondaryColor": COLOR_PALETTE["charcoal"],
    "tertiaryColor": SURFACE_BG,
    # Flowchart / Graph Nodes
    "nodeBorder": BORDER_CYAN_GLOW,
    "nodeTextColor": TEXT_PRIMARY,
    "mainBkg": SURFACE_CARD,
    "clusterBkg": SURFACE_BG,
    "clusterBorder": BORDER_DEFAULT,
    "defaultLinkColor": COLOR_PALETTE["node-3"],
    "titleColor": TEXT_ACCENT,
    "edgeLabelBackground": SURFACE_CARD,
    # Sequence / Actors
    "actorBkg": SURFACE_CARD,
    "actorBorder": COLOR_PALETTE["node-3"],
    "actorTextColor": TEXT_PRIMARY,
    "actorLineColor": COLOR_PALETTE["periwinkle_blue"],
    "signalColor": BORDER_CYAN_GLOW,
    "signalTextColor": TEXT_PRIMARY,
    "labelBoxBkgColor": SURFACE_CARD,
    "labelBoxBorderColor": COLOR_PALETTE["bright_purple"],
    "labelTextColor": TEXT_PRIMARY,
    "loopTextColor": TEXT_ACCENT,
    "noteBkgColor": COLOR_PALETTE["deep_plum"],
    "noteBorderColor": COLOR_PALETTE["sky_info"],
    "noteTextColor": TEXT_PRIMARY,
    "activationBorderColor": COLOR_PALETTE["bright_purple"],
    "activationBkgColor": COLOR_PALETTE["dark_violet"],
    # Class & State
    "classText": TEXT_PRIMARY,
    "stateBkg": SURFACE_CARD,
    "stateBorder": COLOR_PALETTE["node-6"],
    # Git Graph / Branches
    "git0": COLOR_PALETTE["node-2"],
    "git1": COLOR_PALETTE["bright_purple"],
    "git2": COLOR_PALETTE["success_emerald"],
    "git3": COLOR_PALETTE["warning_amber"],
    "git4": COLOR_PALETTE["bright_magenta"],
    "git5": COLOR_PALETTE["sky_info"],
    "git6": COLOR_PALETTE["coral_orange"],
    "git7": COLOR_PALETTE["periwinkle_blue"],
    "gitBranchLabel0": TEXT_PRIMARY,
    "gitBranchLabel1": TEXT_PRIMARY,
    "gitBranchLabel2": TEXT_PRIMARY,
    "gitBranchLabel3": TEXT_PRIMARY,
    # Pie & Sankey
    "pie1": COLOR_PALETTE["node-2"],
    "pie2": COLOR_PALETTE["node-3"],
    "pie3": COLOR_PALETTE["node-6"],
    "pie4": COLOR_PALETTE["bright_purple"],
    "pie5": COLOR_PALETTE["bright_magenta"],
    "pie6": COLOR_PALETTE["success_emerald"],
    "pie7": COLOR_PALETTE["warning_amber"],
    "pieTitleText": TEXT_ACCENT,
    "pieSectionText": COLOR_PALETTE["ghost_white"],
    "pieLegendText": TEXT_PRIMARY,
}

# Standard Eigenscribe Mermaid Class Definitions (CSS-in-Mermaid)
EIGENSCRIBE_MERMAID_CLASSES: Final[dict[str, str]] = {
    "eigenCyan": f"fill:{COLOR_PALETTE['deep_ocean_blue']},stroke:{BORDER_CYAN_GLOW},stroke-width:2px,color:{TEXT_PRIMARY}",
    "eigenSky": f"fill:{COLOR_PALETTE['midnight_navy']},stroke:{COLOR_PALETTE['node-3']},stroke-width:2px,color:{TEXT_PRIMARY}",
    "eigenBlue": f"fill:{COLOR_PALETTE['deep_ocean_blue']},stroke:{COLOR_PALETTE['sky_blue']},stroke-width:2px,color:{TEXT_PRIMARY}",
    "eigenPurple": f"fill:{COLOR_PALETTE['deep_plum']},stroke:{COLOR_PALETTE['bright_purple']},stroke-width:2px,color:{TEXT_PRIMARY}",
    "eigenViolet": f"fill:{COLOR_PALETTE['deep_plum']},stroke:{COLOR_PALETTE['node-6']},stroke-width:2px,color:{TEXT_PRIMARY}",
    "eigenMagenta": f"fill:{COLOR_PALETTE['black_cherry']},stroke:{COLOR_PALETTE['bright_magenta']},stroke-width:2px,color:{TEXT_PRIMARY}",
    "eigenPink": f"fill:{COLOR_PALETTE['black_cherry']},stroke:{COLOR_PALETTE['vivid_pink']},stroke-width:2px,color:{TEXT_PRIMARY}",
    "eigenEmerald": f"fill:{COLOR_PALETTE['deep_pine']},stroke:{COLOR_PALETTE['success_emerald']},stroke-width:2px,color:{TEXT_PRIMARY}",
    "eigenAmber": f"fill:{COLOR_PALETTE['deep_plum']},stroke:{COLOR_PALETTE['warning_amber']},stroke-width:2px,color:{TEXT_PRIMARY}",
    "eigenCrimson": f"fill:{COLOR_PALETTE['black_cherry']},stroke:{COLOR_PALETTE['error_crimson']},stroke-width:2px,color:{TEXT_PRIMARY}",
    "eigenGlass": f"fill:{SURFACE_CARD},stroke:{BORDER_DEFAULT},stroke-width:1.5px,color:{TEXT_PRIMARY}",
    "eigenSubtle": f"fill:{SURFACE_BG},stroke:{SURFACE_ELEVATED},stroke-width:1px,color:{TEXT_MUTED}",
}


# -----------------------------------------------------------------------------------------------------------
# 1️⃣ Public API
# -----------------------------------------------------------------------------------------------------------


def get_mermaid_theme_variables(
    variant: str = "dark",
    **overrides: Any,
) -> dict[str, str]:
    """
    Generate the dictionary of Mermaid theme variables matching the Eigenscribe aesthetic.

    Parameters
    ----------
    variant : str, default="dark"
        Theme variant ("dark", "cosmic", or "high-contrast").
    **overrides : Any
        Custom key-value overrides for specific Mermaid theme variables.

    Returns
    -------
    dict[str, str]
        Dictionary of themeVariable options for Mermaid.js.
    """
    config = dict(EIGENSCRIBE_MERMAID_THEME_VARIABLES)
    if variant == "cosmic":
        config.update({
            "background": COLOR_PALETTE["cosmic_void"],
            "primaryColor": COLOR_PALETTE["cosmic_center"],
            "lineColor": COLOR_PALETTE["electric_cyan"],
            "nodeBorder": COLOR_PALETTE["electric_cyan"],
            "clusterBkg": COLOR_PALETTE["cosmic_void"],
            "clusterBorder": COLOR_PALETTE["deep_ocean_blue"],
        })
    elif variant == "high-contrast":
        config.update({
            "background": COLOR_PALETTE["pure_black"],
            "primaryColor": COLOR_PALETTE["ibm_black"],
            "lineColor": COLOR_PALETTE["node-1"],
            "nodeBorder": COLOR_PALETTE["node-1"],
            "primaryTextColor": COLOR_PALETTE["ghost_white"],
            "clusterBkg": COLOR_PALETTE["ibm_black"],
            "clusterBorder": COLOR_PALETTE["ghost_white"],
        })

    config.update(overrides)
    return config


def get_mermaid_init_directive(
    variant: str = "dark",
    **overrides: Any,
) -> str:
    """
    Generate the `%%{init: {...}}%%` directive block for Mermaid diagrams.

    Parameters
    ----------
    variant : str, default="dark"
        Theme variant name ("dark", "cosmic", or "high-contrast").
    **overrides : Any
        Custom overrides for Mermaid theme variables.

    Returns
    -------
    str
        Formatted Mermaid initialization directive string.
    """
    theme_vars = get_mermaid_theme_variables(variant=variant, **overrides)
    init_payload = {
        "theme": "base",
        "themeVariables": theme_vars,
    }
    json_str = json.dumps(init_payload, indent=2)
    return f"%%{{init: {json_str}}}%%\n"


def get_mermaid_class_defs() -> str:
    """
    Generate standard Eigenscribe classDef declarations for use in Mermaid diagrams.

    Returns
    -------
    str
        Multi-line string containing `classDef` definitions.
    """
    lines = ["    %% Eigenscribe Standard Class Definitions"]
    for class_name, style_str in EIGENSCRIBE_MERMAID_CLASSES.items():
        lines.append(f"    classDef {class_name} {style_str};")
    return "\n".join(lines) + "\n"


def wrap_mermaid_diagram(
    diagram_code: str,
    variant: str = "dark",
    include_classes: bool = True,
    title: str | None = None,
    **overrides: Any,
) -> str:
    """
    Wrap a raw Mermaid diagram body with Eigenscribe initialization directives and style classes.

    Parameters
    ----------
    diagram_code : str
        The raw Mermaid diagram string (e.g., `flowchart TD ...`).
    variant : str, default="dark"
        Theme variant.
    include_classes : bool, default=True
        Whether to append the standard Eigenscribe `classDef` declarations.
    title : str | None, optional
        Optional title header comment to prepend.
    **overrides : Any
        Theme variable overrides.

    Returns
    -------
    str
        Fully configured Mermaid diagram string ready for rendering.
    """
    clean_diagram = diagram_code.strip()
    init_directive = get_mermaid_init_directive(variant=variant, **overrides)

    title_block = f"--- title: {title} ---\n" if title else ""
    class_block = f"\n{get_mermaid_class_defs()}" if include_classes else ""

    return f"{title_block}{init_directive}\n{clean_diagram}\n{class_block}".strip() + "\n"


def generate_mermaid_flowchart(
    nodes: list[tuple[str, str, str | None]] | None = None,
    edges: list[tuple[str, str, str | None]] | None = None,
    direction: str = "TD",
    title: str | None = None,
    variant: str = "dark",
) -> str:
    """
    Programmatically assemble a styled Eigenscribe flowchart diagram.

    Parameters
    ----------
    nodes : list[tuple[str, str, str | None]] | None, optional
        List of nodes formatted as (node_id, label, class_name_or_None).
        If None, generates a default canonical architecture sample.
    edges : list[tuple[str, str, str | None]] | None, optional
        List of edges formatted as (source_id, target_id, edge_label_or_None).
        If None, connects default sample nodes.
    direction : str, default="TD"
        Flowchart direction: "TD", "LR", "BT", "RL".
    title : str | None, optional
        Diagram title.
    variant : str, default="dark"
        Theme variant.

    Returns
    -------
    str
        Complete styled Mermaid flowchart.
    """
    if nodes is None:
        nodes = [
            ("A", "System Ingest", "eigenCyan"),
            ("B", "Deterministic Core", "eigenBlue"),
            ("C", "Visualization Engine", "eigenPurple"),
            ("D", "Telemetry Output", "eigenPink"),
        ]
    if edges is None:
        edges = [
            ("A", "B", "Ingest"),
            ("B", "C", "Process"),
            ("C", "D", "Render"),
        ]

    lines = [f"flowchart {direction}"]

    # Nodes
    for node_id, label, _ in nodes:
        clean_label = label.replace('"', '\\"')
        lines.append(f'    {node_id}["{clean_label}"]')

    lines.append("")

    # Edges
    for src, tgt, edge_label in edges:
        if edge_label:
            clean_edge = edge_label.replace('"', '\\"')
            lines.append(f'    {src} -->|"{clean_edge}"| {tgt}')
        else:
            lines.append(f"    {src} --> {tgt}")

    lines.append("")

    # Class assignments
    class_assignments: list[str] = []
    for node_id, _, cls_name in nodes:
        if cls_name:
            class_assignments.append(f"    class {node_id} {cls_name};")

    if class_assignments:
        lines.extend(class_assignments)

    body = "\n".join(lines)
    return wrap_mermaid_diagram(body, variant=variant, title=title)


def render_html_preview(
    mermaid_code: str,
    title: str = "Eigenscribe Mermaid Diagram",
    theme_variant: str = "dark",
) -> str:
    """
    Generate a standalone HTML page with Mermaid.js CDN to view the diagram in a browser.

    Parameters
    ----------
    mermaid_code : str
        The mermaid diagram code.
    title : str, default="Eigenscribe Mermaid Diagram"
        HTML page title.
    theme_variant : str, default="dark"
        Visual styling backdrop.

    Returns
    -------
    str
        HTML page source code.
    """
    escaped_code = mermaid_code.strip()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <style>
    :root {{
      --bg: {SURFACE_BG};
      --card: {SURFACE_CARD};
      --border: {BORDER_DEFAULT};
      --text: {TEXT_PRIMARY};
      --cyan: {BORDER_CYAN_GLOW};
    }}
    body {{
      background: radial-gradient(circle at center, {COLOR_PALETTE['cosmic_center']} 0%, {COLOR_PALETTE['cosmic_void']} 60%, {COLOR_PALETTE['pure_black']} 100%);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      margin: 0;
      padding: 2rem;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      box-sizing: border-box;
    }}
    .container {{
      background: {_rgba('card_black', 0.85)};
      backdrop-filter: blur(12px);
      border: 1px solid {_rgba('ghost_white', 0.1)};
      border-radius: 12px;
      box-shadow: 0 8px 32px {_rgba('pure_black', 0.5)}, 0 0 16px {_rgba('node-2', 0.15)};
      padding: 2.5rem;
      max-width: 90vw;
      overflow-x: auto;
    }}
    h1 {{
      color: {TEXT_ACCENT};
      font-size: 1.5rem;
      font-weight: 600;
      margin-top: 0;
      margin-bottom: 1.5rem;
      text-align: center;
      text-shadow: 0 0 12px {_rgba('node-2', 0.4)};
    }}
    .mermaid {{
      display: flex;
      justify-content: center;
    }}
  </style>
  <script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
    mermaid.initialize({{ startOnLoad: true, securityLevel: 'loose' }});
  </script>
</head>
<body>
  <div class="container">
    <h1>{title}</h1>
    <div class="mermaid">
{escaped_code}
    </div>
  </div>
</body>
</html>
"""


def save_mermaid_diagram(
    mermaid_code: str,
    file_path: str | Path,
    as_html: bool = False,
    title: str = "Diagram",
) -> Path:
    """
    Save a Mermaid diagram to a file (.mmd, .md, or .html).

    Parameters
    ----------
    mermaid_code : str
        Mermaid diagram code.
    file_path : str | Path
        Destination file path.
    as_html : bool, default=False
        If True, renders and saves as a standalone HTML viewer file.
    title : str, default="Diagram"
        Title if rendered as HTML.

    Returns
    -------
    Path
        The written Path object.
    """
    out_path = Path(file_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if as_html:
        content = render_html_preview(mermaid_code, title=title)
    else:
        content = mermaid_code

    out_path.write_text(content, encoding="utf-8")
    return out_path


# -----------------------------------------------------------------------------------------------------------
# 💨 Smoke Tests
# -----------------------------------------------------------------------------------------------------------


def _run_smoke_test() -> None:
    """Verify theme generation, init directives, and diagram wrapping."""
    print("💨 Running mermaid theme.py smoke tests...")

    # 1. Theme variables verification
    theme_vars = get_mermaid_theme_variables(variant="dark")
    assert theme_vars["darkMode"] == "true"
    assert theme_vars["primaryBorderColor"] == COLOR_PALETTE["node-2"]
    assert "nodeBorder" in theme_vars

    cosmic_vars = get_mermaid_theme_variables(variant="cosmic")
    assert cosmic_vars["background"] == COLOR_PALETTE["cosmic_void"]

    # 2. Init directive check
    directive = get_mermaid_init_directive()
    assert "%%{init:" in directive
    assert "themeVariables" in directive

    # 3. Class defs check
    class_defs = get_mermaid_class_defs()
    assert "classDef eigenCyan" in class_defs
    assert "classDef eigenPurple" in class_defs

    # 4. Wrap diagram check
    raw = "flowchart TD\n    A[Start] --> B[Finish]"
    wrapped = wrap_mermaid_diagram(raw, title="Sample Flow")
    assert "flowchart TD" in wrapped
    assert "%%{init:" in wrapped
    assert "classDef eigenCyan" in wrapped

    # 5. Programmatic generator check
    nodes = [
        ("A", "Initiate Simulation", "eigenCyan"),
        ("B", "Integrate Dynamics", "eigenPurple"),
        ("C", "Compute Observables", "eigenEmerald"),
    ]
    edges = [
        ("A", "B", "Initialize"),
        ("B", "C", "Order Parameter"),
    ]
    generated = generate_mermaid_flowchart(nodes, edges, title="Kuramoto Flow")
    assert "flowchart TD" in generated
    assert 'A["Initiate Simulation"]' in generated
    assert "class A eigenCyan;" in generated

    # 6. HTML preview renderer
    html = render_html_preview(generated, title="Preview Test")
    assert "<!DOCTYPE html>" in html
    assert "mermaid.initialize" in html

    print("✅ mermaid theme.py smoke tests passed.")


# -----------------------------------------------------------------------------------------------------------
# 🔥 Entry Point
# -----------------------------------------------------------------------------------------------------------


def main() -> None:
    """Execute module smoke tests."""
    _run_smoke_test()


if __name__ == "__main__":
    main()
