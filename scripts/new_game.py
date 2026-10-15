#!/usr/bin/env python3
"""Deriva um projeto HTML5 standalone do vertical slice de PocketForge."""
import argparse
import html
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "demo"


def create_game(destination: Path, title: str) -> Path:
    destination = destination.expanduser().resolve()
    if destination.exists():
        raise FileExistsError(f"Destino já existe: {destination}")
    if not title.strip():
        raise ValueError("O título não pode ser vazio")
    shutil.copytree(TEMPLATE, destination)
    name = html.escape(title.strip())
    page = destination / "index.html"
    page.write_text(
        page.read_text(encoding="utf-8")
        .replace("LUMEN SHIFT", name.upper())
        .replace("Lumen Shift", name),
        encoding="utf-8",
    )
    game = destination / "game.js"
    source = game.read_text(encoding="utf-8")
    source = source.replace(
        '"Lumen <em>Shift</em>"',
        json.dumps(name, ensure_ascii=False),
    )
    game.write_text(source, encoding="utf-8")
    (destination / "README.md").write_text(
        "# " + title.strip() + "\n\n"
        "Criado com PocketForge, a partir do vertical slice Lumen Shift.\n\n"
        "Executar: `python3 -m http.server 8000 --directory .`\n\n"
        "**Importante:** este scaffold herda as mecânicas do exemplo.\n"
        "Customize gameplay, assets e testes para criar um jogo próprio.\n",
        encoding="utf-8",
    )
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path, help="Pasta nova de destino")
    parser.add_argument("--title", default="PocketForge Game", help="Título do jogo")
    args = parser.parse_args()
    try:
        folder = create_game(args.destination, args.title)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print("Jogo criado em:", folder)
    return 0


if __name__ == "__main__":
    sys.exit(main())
