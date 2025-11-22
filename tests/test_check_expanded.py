from __future__ import annotations

from pathlib import Path

from neurocode.check import check_file
from neurocode.config import load_config
from neurocode.ir_build import build_repository_ir


def _write_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "mod_cycle.py").write_text(
        "def a(x):\n"
        "    return b(x)\n"
        "\n"
        "def b(y):\n"
        "    return a(y)\n",
        encoding="utf-8",
    )
    (repo / "mod_params.py").write_text(
        "def foo(x, y):\n"
        "    return x + 1\n",
        encoding="utf-8",
    )
    (repo / "mod_long.py").write_text(
        "def long_fn(z):\n"
        "    one = z + 1\n"
        "    two = one + 1\n"
        "    three = two + 1\n"
        "    four = three + 1\n"
        "    return four\n",
        encoding="utf-8",
    )
    (repo / ".neurocoderc").write_text(
        "long_function_threshold = 4\n"
        "enabled_checks = [\"UNUSED_PARAM\", \"LONG_FUNCTION\", \"CALL_CYCLE\"]\n",
        encoding="utf-8",
    )
    return repo


def test_expanded_checks_detect_issues(tmp_path: Path) -> None:
    repo = _write_repo(tmp_path)
    ir = build_repository_ir(repo)
    config = load_config(repo)

    # Unused param and long function.
    params_path = repo / "mod_params.py"
    results_params = check_file(ir=ir, repo_root=repo, file=params_path, config=config)
    codes = {r.code for r in results_params}
    assert "UNUSED_PARAM" in codes

    long_path = repo / "mod_long.py"
    results_long = check_file(ir=ir, repo_root=repo, file=long_path, config=config)
    codes_long = {r.code for r in results_long}
    assert "LONG_FUNCTION" in codes_long

    # Call cycle.
    cycle_path = repo / "mod_cycle.py"
    results_cycle = check_file(ir=ir, repo_root=repo, file=cycle_path, config=config)
    codes_cycle = {r.code for r in results_cycle}
    assert "CALL_CYCLE" in codes_cycle
