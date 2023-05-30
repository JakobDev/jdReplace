#!/usr/bin/env python
import subprocess
import pathlib
import shutil
import sys


def main() -> None:
    if not shutil.which("pylupdate6"):
        print("pylupdate6 was not found", file=sys.stderr)
        sys.exit(1)

    for i in (pathlib.Path(__file__).parent.parent / "jdReplace" / "translations").iterdir():
        if i.suffix == ".ts":
            subprocess.run(["pylupdate6", "jdReplace", "--ts", str(i), "--no-obsolete"], cwd=pathlib.Path(__file__).parent.parent)


if __name__ == "__main__":
    main()
