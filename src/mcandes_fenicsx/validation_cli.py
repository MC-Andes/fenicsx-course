"""Validador instalable para fichas, scripts y enlaces documentales."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import unquote

from mcandes_fenicsx.metadata import load_metadata

_EXAMPLE_REFERENCE = re.compile(r"examples/[A-Za-z0-9_./-]+\.py")
_MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def validate_repository(root: Path) -> list[str]:
    errors: list[str] = []
    metadata_dir = root / "examples" / "metadata"
    seen_ids: set[str] = set()
    described_scripts: set[str] = set()
    for path in sorted(metadata_dir.glob("*.yml")):
        try:
            item = load_metadata(path)
        except (OSError, ValueError) as exc:
            errors.append(f"{path.relative_to(root)}: {exc}")
            continue
        if item.identifier in seen_ids:
            errors.append(f"id duplicado: {item.identifier}")
        seen_ids.add(item.identifier)
        described_scripts.add(item.script)
        script = root / item.script
        if not script.is_file():
            errors.append(f"script ausente: {item.script}")
        if item.script not in item.command:
            errors.append(f"command no ejecuta el script canónico: {path.name}")

    scripts = {
        str(path.relative_to(root))
        for path in (root / "examples").glob("[0-9][0-9]_*.py")
    }
    for missing in sorted(scripts - described_scripts):
        errors.append(f"metadata ausente para {missing}")

    for doc in (root / "docs").rglob("*.md"):
        text = doc.read_text(encoding="utf-8")
        for reference in _EXAMPLE_REFERENCE.findall(text):
            if not (root / reference).is_file():
                errors.append(f"{doc.relative_to(root)} referencia ruta ausente: {reference}")
        for raw_target in _MARKDOWN_LINK.findall(text):
            target = raw_target.split("#", maxsplit=1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            candidate = (doc.parent / unquote(target)).resolve()
            if not candidate.exists():
                errors.append(
                    f"{doc.relative_to(root)} referencia enlace local ausente: {raw_target}"
                )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    args = parser.parse_args()
    errors = validate_repository(args.root.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Fichas, scripts y enlaces documentales: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
