"""Build portable native bundles from reviewed source by Jason Stys.

Function: main. Variables: root, slug, executable, PyInstaller command, zip manifest.
Generated bundles are unsigned; exact symbols: docs/CODE_INDEX.md. No installer/elevation.
"""

import hashlib
import platform
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    """Freeze the existing production web build, smoke it, then zip this platform's bundle."""
    root = Path(__file__).resolve().parents[1]
    if not (root / "web/dist/index.html").is_file():
        raise SystemExit("Run npm ci and npm run build first")
    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--onedir",
        "--console",
        "--name",
        "OrbitalSafetyWorkbench",
        "--add-data",
        "web/dist:web/dist",
        "--add-data",
        "orbital/resources:orbital/resources",
        "--copy-metadata",
        "sgp4",
        "--add-data",
        "LICENSE:licenses/project",
        "--add-data",
        "node_modules/three/LICENSE:licenses/three",
        "--add-data",
        "docs/THIRD_PARTY.md:docs",
        "launcher.py",
    ]
    subprocess.run(command, cwd=root, check=True, timeout=600)
    executable = (
        root
        / "dist/OrbitalSafetyWorkbench"
        / ("OrbitalSafetyWorkbench.exe" if sys.platform == "win32" else "OrbitalSafetyWorkbench")
    )
    subprocess.run(
        [sys.executable, "tools/smoke_app.py", str(executable)], cwd=root, check=True, timeout=90
    )
    slug = f"orbital-safety-workbench-{platform.system().lower()}-{platform.machine().lower()}"
    archive = Path(
        shutil.make_archive(
            str(root / "dist" / slug), "zip", root / "dist", "OrbitalSafetyWorkbench"
        )
    )
    with archive.open("rb") as source:
        digest = hashlib.file_digest(source, "sha256").hexdigest()
    (root / "dist" / f"{slug}.sha256").write_text(f"{digest}  {archive.name}\n", encoding="utf-8")
    print(f"Portable bundle verified: {archive.name} SHA-256 {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
