#!/usr/bin/env python3
"""Copy the reviewed local skill into an explicitly selected skill directory."""
import argparse
import shutil
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-dir", required=True, type=Path,
                        help="Agent-discovered skill directory for this environment")
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1] / "plugins/kpri/skills/design-reference"
    destination = args.skills_dir.expanduser().resolve() / "design-reference"
    files = sorted(p for p in source.rglob("*") if p.is_file())
    if not files or not (source / "SKILL.md").is_file():
        parser.error("Source skill is missing.")
    for path in files:
        target = destination / path.relative_to(source)
        if target.is_symlink() or any(parent.is_symlink() for parent in target.parents):
            parser.error(f"Refusing symlink destination: {target}")
        if target.exists() and (not target.is_file() or target.read_bytes() != path.read_bytes()):
            parser.error(f"Existing file differs; review before replacing: {target}")
    for path in files:
        target = destination / path.relative_to(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            shutil.copyfile(path, target)
    print(f"Installed {len(files)} files in {destination}")
    print("Reload skills or start a new agent turn to confirm discovery.")

if __name__ == "__main__":
    main()
