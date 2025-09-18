from .base import Finding


def _pragma_allows_checks(ast):
    try:
        for child in ast.get('children', []):
            if child.get('type') == 'PragmaDirective' and 'solidity' in child.get('name', ''):
                val = child.get('value', '')
                if '0.8' in val or '>=0.8' in val or '^0.8' in val:
                    return True
    except Exception:
        pass
    return False


def find_integer_overflow(ast, filename="<input>"):
    findings = []
    if _pragma_allows_checks(ast):
        return findings

    def recurse(node):
        if isinstance(node, dict):
            if node.get('type') == 'BinaryOperation':
                op = node.get('operator')
                if op in ['+', '-', '*']:
                    line = node.get('loc', {}).get('start', {}).get('line', -1)
                    f = Finding(
                        id='I001',
                        name='Integer Overflow/Underflow (possible)',
                        severity='High',
                        description=f'Found arithmetic operator {op} in pragma <0.8.0 context; consider SafeMath or upgrade to ^0.8.0',
                        file=filename,
                        line=line,
                        evidence=f'Operator {op} at line {line}',
                        recommendation='Upgrade to Solidity >=0.8.0 or use SafeMath and add unit tests.'
                    )
                    findings.append(f.to_dict())
            for v in node.values():
                recurse(v)
        elif isinstance(node, list):
            for e in node:
                recurse(e)
    recurse(ast)
    return findings

