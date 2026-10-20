"""Standalone application entry by Jason Stys; main is the documented CLI entry.

Variables: argv supplies default serve mode for a double-click launch.
Line inventory: docs/CODE_INDEX.md. No elevation, service installation or auto-update.
"""

import sys

from orbital.__main__ import main

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:] or ["serve"]))
