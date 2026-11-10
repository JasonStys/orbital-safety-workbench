"""Build and verify versioned portable applications by Jason Stys.

Function: main. Variables: config, source metadata, fixed worker and owned extraction directory.
Only the actual extracted binary is accepted. Exact lines: docs/CODE_INDEX.md. No installer hooks.
"""

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from importlib.metadata import distribution
from pathlib import Path

if __package__:
    from .portable_archive import archive_metadata, create_archive, extract_archive
    from .release_contract import ROOT, asset_paths, configuration, require, source_metadata
else:
    from portable_archive import archive_metadata, create_archive, extract_archive
    from release_contract import ROOT, asset_paths, configuration, require, source_metadata


def main() -> int:
    """Build from pinned dependencies, preserve native archive semantics, then exercise extracted UI."""
    parser = argparse.ArgumentParser(
        description="Build and test this platform's portable application"
    )
    parser.add_argument("--output-root", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    config, metadata = configuration(), source_metadata()
    require((ROOT / "web/dist/index.html").is_file(), "Build production web assets first")
    generated = ROOT / ".runtime/package-meta"
    generated.mkdir(parents=True, exist_ok=True)
    identity = generated / "RELEASE.json"
    identity.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    executable_name = config["executable"]
    root = ROOT
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
    installer = distribution("pyinstaller")
    notices = [
        installer.locate_file(file)
        for file in installer.files or []
        if str(file).endswith("licenses/COPYING.txt")
    ]
    require(len(notices) == 1, "Expected pinned PyInstaller license")
    command[command.index("launcher.py") : command.index("launcher.py")] = [
        "--add-data",
        "licenses/PYTHON.txt:licenses/python",
        "--add-data",
        str(notices[0]) + ":licenses/pyinstaller",
        "--add-data",
        str(identity) + ":orbital/resources",
    ]
    subprocess.run(command, cwd=ROOT, check=True, timeout=600)
    bundle = ROOT / "dist" / executable_name
    shutil.copyfile(identity, bundle / "RELEASE.json")
    archive, checksum = asset_paths(metadata)
    archive, checksum = (
        args.output_root.resolve() / archive.name,
        args.output_root.resolve() / checksum.name,
    )
    archive.parent.mkdir(parents=True, exist_ok=True)
    require(not checksum.exists(), "Checksum destination already exists")
    create_archive(bundle, archive)
    require(
        archive_metadata(archive, executable_name) == metadata, "Created archive identity mismatch"
    )
    with tempfile.TemporaryDirectory(prefix="flight-extracted-") as temporary:
        extracted = extract_archive(archive, Path(temporary) / "unpacked", executable_name)
        executable = extracted / (executable_name + (".exe" if sys.platform == "win32" else ""))
        subprocess.run(
            [sys.executable, str(ROOT / "tools/smoke_app.py"), str(executable)],
            cwd=temporary,
            check=True,
            timeout=120,
        )
    with archive.open("rb") as source:
        digest = hashlib.file_digest(source, "sha256").hexdigest()
    checksum.write_text(f"{digest}  {archive.name}\n", encoding="utf-8")
    print(f"Extracted portable application passed: {archive.name} SHA-256 {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
