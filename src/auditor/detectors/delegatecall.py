from .base import Finding


def find_delegatecall(ast, filename="<input>"):
    findings = []

    def recurse(node):
        if isinstance(node, dict):
            if node.get('type') == 'FunctionCall':
                callee = node.get('expression')
                if callee and callee.get('type') == 'MemberAccess':
                    member = callee.get('memberName')
                    if member == 'delegatecall':
                        line = node.get('loc', {}).get('start', {}).get('line', -1)
                        f = Finding(
                            id='D001',
                            name='delegatecall usage',
                            severity='High',
                            description='delegatecall can be dangerous; it executes in the context of the caller.',
                            file=filename,
                            line=line,
                            evidence='delegatecall found',
                            recommendation='Avoid delegatecall unless necessary; validate target and data strictly.'
                        )
                        findings.append(f.to_dict())
            for v in node.values():
                recurse(v)
        elif isinstance(node, list):
            for e in node:
                recurse(e)

    recurse(ast)
    return findings

