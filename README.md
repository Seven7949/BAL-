# sol-auditor (MVP)

A minimal Smart Contract Auditor focused on static AST checks. This MVP scans Solidity source files for common issues (reentrancy, integer overflow for <0.8.0, unchecked low-level calls, tx.origin, delegatecall usage) and produces JSON + HTML reports.

Optional: If you have Slither or Mythril installed, the CLI can call them to supplement findings.

## Quickstart

1. Create virtualenv and install base deps:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. (Optional) Install Slither (requires pipx) and Mythril (optional heavy dependency):

```bash
# recommended: use pipx for slither
pipx install slither-analyzer
# mythril via pip (may require OS deps)
pip install mythril
```

3. Run the sample scan:

```bash
PYTHONPATH=src python -m auditor.cli examples/vulnerable_contracts.sol --json report.json --html report.html
```

4. Run tests:

```bash
PYTHONPATH=src pytest -q
```

## How to extend

- Add detectors under `src/auditor/detectors/`
- Expand AST parsing/resolution for fewer false positives.

## Notes

- Static AST detectors run by default.
- Use `--slither` or `--mythril` flags to run optional backends if installed:

```bash
PYTHONPATH=src python -m auditor.cli examples/vulnerable_contracts.sol --slither --mythril --json report.json --html report.html
```

- Heuristic static checks may produce false positives; review findings manually.


