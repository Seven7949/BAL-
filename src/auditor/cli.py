import argparse
import datetime
import subprocess
import json
from .parser import parse_file
from .detectors.reentrancy import find_reentrancy
from .detectors.integer_overflow import find_integer_overflow
from .detectors.unchecked_calls import find_unchecked_calls
from .detectors.tx_origin import find_tx_origin
from .detectors.delegatecall import find_delegatecall
from .report import generate_json_report, generate_html_report


def run_slither(path):
    try:
        res = subprocess.run(['slither', '--json', 'slither-out.json', path], capture_output=True, text=True, check=False)
        import os
        if os.path.exists('slither-out.json'):
            with open('slither-out.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            return [{'id': 'SL001', 'name': 'Slither output', 'severity': 'Info', 'description': str(data), 'file': path, 'line': -1}]
    except FileNotFoundError:
        print('Slither not installed or not in PATH')
    except Exception as e:
        print('Error running slither:', e)
    return []


def run_mythril(path):
    try:
        res = subprocess.run(['myth', 'analyze', path, '--output', 'json', '--silent'], capture_output=True, text=True, check=False)
        if res.stdout:
            try:
                data = json.loads(res.stdout)
                return [{'id': 'MY001', 'name': 'Mythril output', 'severity': 'Info', 'description': str(data), 'file': path, 'line': -1}]
            except Exception:
                return [{'id': 'MY001', 'name': 'Mythril raw', 'severity': 'Info', 'description': res.stdout, 'file': path, 'line': -1}]
    except FileNotFoundError:
        print('Mythril (myth) not installed')
    except Exception as e:
        print('Error running mythril:', e)
    return []


def main():
    parser = argparse.ArgumentParser(prog='auditor', description='sol-auditor CLI')
    parser.add_argument('contract', help='Solidity file to scan')
    parser.add_argument('--json', help='Output JSON path', default=None)
    parser.add_argument('--html', help='Output HTML path', default=None)
    parser.add_argument('--slither', help='Run Slither if installed', action='store_true')
    parser.add_argument('--mythril', help='Run Mythril if installed', action='store_true')
    args = parser.parse_args()

    ast = parse_file(args.contract)
    findings = []
    findings.extend(find_reentrancy(ast, args.contract))
    findings.extend(find_integer_overflow(ast, args.contract))
    findings.extend(find_unchecked_calls(ast, args.contract))
    findings.extend(find_tx_origin(ast, args.contract))
    findings.extend(find_delegatecall(ast, args.contract))

    if args.slither:
        findings.extend(run_slither(args.contract))
    if args.mythril:
        findings.extend(run_mythril(args.contract))

    meta = {
        'scanner': 'sol-auditor v0.2',
        'scanned_at': datetime.datetime.utcnow().isoformat() + 'Z',
        'target': args.contract
    }

    if args.json:
        generate_json_report(meta, findings, args.json)
        print(f'Wrote JSON report to {args.json}')

    if args.html:
        # html template file is expected to be next to report.py as report_template.html
        generate_html_report(meta, findings, args.html)
        print(f'Wrote HTML report to {args.html}')

    if not args.json and not args.html:
        import json
        print(json.dumps({'meta': meta, 'findings': findings}, indent=2))


if __name__ == '__main__':
    main()

