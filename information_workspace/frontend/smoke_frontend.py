from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    script = Path(__file__).with_name("smoke_frontend.js")
    proc = subprocess.run(["node", str(script), *sys.argv[1:]], text=True, check=False)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
