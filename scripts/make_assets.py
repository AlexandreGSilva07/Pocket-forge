#!/usr/bin/env python3
"""Gera assets vetoriais abstratos de autoria procedural (não spritesheets)."""
import argparse
import json
from pathlib import Path
import random
import sys


def generate(destination: Path, seed: int = 42) -> list:
    rng = random.Random(seed)
    destination.mkdir(parents=True, exist_ok=True)
    colors = ["#56e8ee", "#ed75b6", "#a48cff", "#92f3bd", "#f9d47c"]
    templates = {
        "core.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
<defs><radialGradient id="g"><stop stop-color="#edffff"/><stop offset=".48" stop-color="COLOR"/><stop offset="1" stop-color="#154b65"/></radialGradient></defs>
<circle cx="64" cy="64" r="44" fill="url(#g)" opacity=".4"/>
<path d="M64 11 91 64 64 117 37 64Z" fill="COLOR" stroke="#e9ffff" stroke-width="3"/>
<circle cx="64" cy="64" r="12" fill="#fff"/>
</svg>""",
        "enemy.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
<path d="M64 4 96 28 124 64 96 100 64 124 32 100 4 64 32 28Z" fill="#491d4f" stroke="COLOR" stroke-width="5"/>
<path d="M64 25 103 64 64 103 25 64Z" fill="COLOR" opacity=".75"/>
<circle cx="64" cy="64" r="12" fill="#fff4fa"/>
</svg>""",
        "pickup.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
<circle cx="64" cy="64" r="49" stroke="COLOR" stroke-width="5" fill="none"/>
<path d="M64 21 76 52 107 64 76 76 64 107 52 76 21 64 52 52Z" fill="COLOR"/>
<circle cx="64" cy="64" r="9" fill="white"/>
</svg>""",
    }
    manifest = []
    for name, template in templates.items():
        color = colors[rng.randrange(len(colors))]
        (destination / name).write_text(template.replace("COLOR", color) + "\n", encoding="utf-8")
        manifest.append({
            "id": name.removesuffix(".svg"), "kind": "svg", "path": name,
            "logicalSize": [128, 128], "source": "PocketForge procedural", "license": "MIT",
            "seed": seed, "color": color
        })
    # Fundo com composição procedural sem filtros caros.
    blocks = []
    for _ in range(24):
        x, y = rng.randrange(0, 800), rng.randrange(0, 600)
        radius = rng.randrange(8, 110)
        color = colors[rng.randrange(len(colors))]
        blocks.append(f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{color}" opacity=".075"/>')
    background = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600">'
                  '<rect width="800" height="600" fill="#081021"/>'
                  + "".join(blocks) + '</svg>\n')
    (destination / "background.svg").write_text(background, encoding="utf-8")
    manifest.append({
        "id": "background", "kind": "svg", "path": "background.svg",
        "logicalSize": [800, 600], "source": "PocketForge procedural", "license": "MIT", "seed": seed
    })
    (destination / "manifest.json").write_text(
        json.dumps({"schemaVersion": "0.1", "assets": manifest}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    manifest = generate(args.destination, args.seed)
    print(f"{len(manifest)} SVGs gerados em {args.destination}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
