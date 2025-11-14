from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def _run_cli(project_root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "neurocode.cli", *args],
        cwd=project_root,
        capture_output=True,
        text=True,
    )


def test_cli_check_info_only_returns_zero(repo_with_ir: Path, project_root: Path) -> None:
    target_file = repo_with_ir / "package" / "mod_b.py"
    result = _run_cli(project_root, "check", str(target_file))

    assert result.returncode == 0, result.stdout
    assert any(
        line.startswith("INFO UNUSED_FUNCTION")
        for line in result.stdout.splitlines()
        if line.strip()
    )


def test_cli_check_reports_no_issues_message(tmp_path: Path, project_root: Path) -> None:
    repo = tmp_path / "clean_repo"
    repo.mkdir()
    module_path = repo / "clean_mod.py"
    module_path.write_text(
        (
            "def helper() -> int:\n"
            "    return 42\n\n"
            "def entrypoint() -> int:\n"
            "    return helper()\n\n"
            "def _driver() -> int:\n"
            "    return entrypoint()\n"
        ),
        encoding="utf-8",
    )

    ir_result = _run_cli(project_root, "ir", str(repo))
    assert ir_result.returncode == 0, ir_result.stderr

    result = _run_cli(project_root, "check", str(module_path))
    assert result.returncode == 0, result.stderr
    assert "[neurocode] No issues found." in result.stdout


def test_cli_check_without_ir_errors(sample_repo: Path, project_root: Path) -> None:
    target_file = sample_repo / "package" / "mod_a.py"

    result = _run_cli(project_root, "check", str(target_file))
    assert result.returncode == 1
    assert "error" in result.stderr.lower()
    assert "ir.toon" in result.stderr
