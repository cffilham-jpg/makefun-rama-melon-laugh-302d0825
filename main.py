"""Write the one-line office joke entry for make.fun."""

import hashlib
import os
import tempfile
from pathlib import Path

LINE = "My inbox is a to-do list written by other people."
CHAR_LIMIT = 200


def _resolve_output_dir() -> Path:
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        path = Path(env_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path
    try:
        out = Path("out")
        out.mkdir(parents=True, exist_ok=True)
        return out
    except OSError:
        return Path(tempfile.mkdtemp(prefix="makefun-rama-melon-laugh-302d0825-"))


def validate(path: Path) -> None:
    data = path.read_bytes()
    text = data.decode("utf-8")
    if text != LINE:
        raise ValueError("entry.txt content does not match LINE")
    if not 1 <= len(text) <= CHAR_LIMIT:
        raise ValueError("line must be 1-200 chars")
    if "\n" in text or "\r" in text:
        raise ValueError("line must be a single line")
    if not text.strip():
        raise ValueError("line must not be only whitespace")


def main() -> None:
    out_dir = _resolve_output_dir()
    target = out_dir / "entry.txt"
    target.write_text(LINE, encoding="utf-8")
    validate(target)
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    print(f"wrote {target} ({len(LINE)} chars, sha256 {digest})")


if __name__ == "__main__":
    main()
