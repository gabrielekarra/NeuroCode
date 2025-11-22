# Changelog

## 0.1.0
- Initial published version with IR generation (`neurocode ir`), explain/check/patch commands, status command, JSON outputs, and configurable checks.
- New diagnostics: unused imports/functions/params/returns, high fan-out, long functions, call cycles, import cycles.
- Config via `.neurocoderc`/`[tool.neurocode]`.
- Patch strategies (guard/todo/inject) with idempotent markers and JSON output.
- IR freshness hashes/timestamp; `ir --check` and `status` command.
- CI workflow (ruff + pytest) and IR schema docs.
