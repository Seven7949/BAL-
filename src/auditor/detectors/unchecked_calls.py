from .base import Finding

UNSAFE_MEMBERS = {"call"}


def find_unchecked_calls(ast, filename="<input>"):
    findings = []

    def recurse(node):
        if isinstance(node, dict):
            if node.get('type') == 'ExpressionStatement':
                expr = node.get('expression')
                if expr and expr.get('type') == 'FunctionCall':
                    callee = expr.get('expression')
                    if callee and callee.get('type') == 'MemberAccess':
                        mem = callee.get('memberName')
                        if mem in UNSAFE_MEMBERS:
                            line = node.get('loc', {}).get('start', {}).get('line', -1)
                            f = Finding(
                                id='U001',
                                name='Unchecked low-level call',
                                severity='High',
                                description='Low-level call returned value may be ignored or unchecked; always check return boolean to avoid silent failures.',
                                file=filename,
                                line=line,
                                evidence=f'Use of {mem} at line {line}',
                                recommendation='Check the returned boolean or handle failures explicitly.'
                            )
                            findings.append(f.to_dict())
            for v in node.values():
                recurse(v)
        elif isinstance(node, list):
            for e in node:
                recurse(e)

    recurse(ast)
    return findings

