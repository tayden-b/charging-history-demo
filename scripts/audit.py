import argparse
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit the complete locked runtime dependency graph."
    )
    parser.add_argument("--output-dir", default="artifacts")
    args = parser.parse_args()
    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)
    requirements = output / "runtime-requirements.txt"
    exported = subprocess.run(
        [
            "uv",
            "export",
            "--locked",
            "--no-dev",
            "--no-emit-project",
            "--format",
            "requirements-txt",
            "--no-hashes",
            "--output-file",
            str(requirements),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if exported.returncode:
        print(exported.stderr, file=sys.stderr)
        return exported.returncode
    print("Scope: all locked runtime dependencies, including transitive dependencies.")
    print("Development tools are outside this check. This is not an application-code scan.")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pip_audit",
            "--requirement",
            str(requirements),
            "--no-deps",
            "--disable-pip",
            "--format",
            "json",
            "--output",
            str(output / "dependency-audit.json"),
        ],
        check=False,
    )
    print(f"Audit exit status: {result.returncode}. Report: {output / 'dependency-audit.json'}")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
