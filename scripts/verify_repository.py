"""Check inventory, SHA-256 integrity and obvious private markers."""

import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path


LEDGER = "SHA256SUMS.txt"
GENERATED_TEX_FILES = {
    "manuscript.aux", "manuscript.bbl", "manuscript.bcf", "manuscript.blg",
    "manuscript.fdb_latexmk", "manuscript.fls", "manuscript.log",
    "manuscript.out", "manuscript.run.xml", "manuscript.synctex.gz",
    "manuscript.toc",
}
BINARY_SUFFIXES = {".pdf", ".png", ".gif", ".zip"}
PRIVATE_MARKERS = {
    "local home path": r"/(?:Users|home)/[^/\s]+/|[A-Za-z]:\\Users\\",
    "private session URL": r"chatgpt\.com/(?:c/|[^)\s]*messageId=)|claude\.ai/(?:chat|code)/",
    "local Codex state": r"[.]codex/|rollout-20\d\d-",
    "GitHub token": r"gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}",
    "API key": r"sk-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{30,}",
    "private-key block": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_path(name):
    if (
        not name
        or name != name.strip()
        or "\\" in name
        or any(ord(char) < 32 for char in name)
        or any(part in {"", ".", "..", ".git"} for part in name.split("/"))
        or name == LEDGER
    ):
        raise ValueError(f"unsafe or reserved inventory path: {name!r}")
    return name


def manifest_paths(root):
    files = set()
    for line in (root / "MANIFEST.md").read_text(encoding="utf-8").splitlines():
        if not line.startswith("- "):
            continue
        match = re.fullmatch(r"- \x60([^\x60]+)\x60", line)
        if not match:
            raise ValueError(f"invalid manifest entry: {line!r}")
        name = validate_path(match[1])
        if name in files:
            raise ValueError(f"duplicate manifest entry: {name}")
        files.add(name)
    if "MANIFEST.md" not in files:
        raise ValueError("MANIFEST.md must list itself")
    return files


def working_tree_paths(root):
    files = set()
    for directory, subdirs, filenames in os.walk(root):
        current = Path(directory)
        subdirs[:] = [name for name in subdirs if name not in {".git", "__pycache__"}]
        for name in subdirs + filenames:
            path = current / name
            relative = path.relative_to(root)
            if path.is_symlink():
                raise ValueError(f"symlink in candidate tree: {relative}")
            if name in {".DS_Store", ".git"} or relative.as_posix() == LEDGER:
                continue
            if path.is_dir() or path.suffix in {".pyc", ".pyo"}:
                continue
            if relative.parent == Path("paper") and name in GENERATED_TEX_FILES:
                continue
            if not path.is_file():
                raise ValueError(f"non-regular candidate path: {relative}")
            files.add(relative.as_posix())
    return files


def require_matching_paths(allowed, observed, label):
    differences = [
        *(f"missing from {label}: {name}" for name in sorted(allowed - observed)),
        *(f"unexpected in {label}: {name}" for name in sorted(observed - allowed)),
    ]
    if differences:
        raise ValueError("\n".join(differences))


def check_inventory(root, paths, *, check_git=True):
    require_matching_paths(paths, working_tree_paths(root), "candidate tree")
    # The private staging trees can sit inside a larger, unrelated repository.
    if check_git and (root / ".git").exists():
        raw = subprocess.check_output(["git", "ls-files", "-z"], cwd=root)
        tracked = {os.fsdecode(name) for name in raw.split(b"\0") if name}
        require_matching_paths(paths | {LEDGER}, tracked, "Git index")


def read_ledger(root):
    ledger = {}
    for line in (root / LEDGER).read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([a-f0-9]{64})  (.+)", line)
        if not match:
            raise ValueError("invalid SHA-256 ledger line")
        checksum, name = match.groups()
        validate_path(name)
        if name in ledger:
            raise ValueError(f"duplicate checksum entry: {name}")
        ledger[name] = checksum
    return ledger


def scan_text(path):
    text = path.read_text(encoding="utf-8")
    return [
        label for label, pattern in PRIVATE_MARKERS.items()
        if re.search(pattern, text, flags=re.IGNORECASE)
    ]


def main():
    root = Path(__file__).resolve().parents[1]
    try:
        paths = manifest_paths(root)
        check_inventory(root, paths)
        ledger = read_ledger(root)
        require_matching_paths(paths, ledger.keys(), LEDGER)

        errors = []
        for name in sorted(paths):
            path = root / name
            if digest(path) != ledger[name]:
                errors.append(f"hash mismatch: {name}")
            if path.suffix not in BINARY_SUFFIXES:
                errors.extend(f"{label} in {name}" for label in scan_text(path))
        if errors:
            raise ValueError("\n".join(errors))
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        sys.exit(str(error))
    print(f"OK: {len(paths)} hashed files, text privacy scan clean")


if __name__ == "__main__":
    main()
