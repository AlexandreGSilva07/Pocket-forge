#!/usr/bin/env python3
"""Audita peso estático local de um jogo. NÃO mede FPS, RAM ou rede real."""
import argparse
from collections import defaultdict
import gzip
import json
from pathlib import Path
import sys

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist-cache"}


def audit(root: Path) -> dict:
    if not root.is_dir():
        raise NotADirectoryError(f"Pasta inválida: {root}")
    files, by_extension = [], defaultdict(lambda: {"files": 0, "bytes": 0, "gzip_bytes": 0})
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        content = path.read_bytes()
        ext = path.suffix.lower() or "[sem extensão]"
        gz = len(gzip.compress(content, compresslevel=9, mtime=0))
        data = {"path": str(path.relative_to(root)), "bytes": len(content), "gzip_bytes": gz}
        files.append(data)
        by_extension[ext]["files"] += 1
        by_extension[ext]["bytes"] += len(content)
        by_extension[ext]["gzip_bytes"] += gz
    return {
        "root": str(root),
        "file_count": len(files),
        "total_bytes": sum(f["bytes"] for f in files),
        "sum_gzip_bytes": sum(f["gzip_bytes"] for f in files),
        "by_extension": dict(sorted(by_extension.items())),
        "files": sorted(files, key=lambda f: f["bytes"], reverse=True),
        "caveat": "gzip por arquivo é estimativa local; não equivale ao tráfego HTTP real ou memória carregada."
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="Diretório do build")
    parser.add_argument("--json", action="store_true", help="Imprimir JSON")
    parser.add_argument("--max-bytes", type=int, default=None, help="Falhar se exceder total de bytes brutos")
    args = parser.parse_args()
    try:
        result = audit(args.directory.resolve())
    except OSError as exc:
        parser.error(str(exc))
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("Arquivos:", result["file_count"])
        print("Tamanho bruto:", result["total_bytes"], "bytes")
        print("Soma de gzip por arquivo:", result["sum_gzip_bytes"], "bytes")
        for ext, group in result["by_extension"].items():
            print(f"  {ext:12} {group['files']:3} arquivos {group['bytes']:8} bytes")
        print(result["caveat"])
    if args.max_bytes is not None and result["total_bytes"] > args.max_bytes:
        print("ORÇAMENTO EXCEDIDO:", result["total_bytes"], ">", args.max_bytes, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
