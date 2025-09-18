from .base import Finding


def find_tx_origin(ast, filename="<input>"):
    findings = []

    def recurse(node):
        if isinstance(node, dict):
            # solidity_parser represents tx.origin as MemberAccess of Identifier 'tx'
            if node.get('type') == 'MemberAccess':
                base = node.get('expression')
                member = node.get('memberName')
                if base and base.get('type') == 'Identifier' and base.get('name') == 'tx' and member == 'origin':
                    line = node.get('loc', {}).get('start', {}).get('line', -1)
                    f = Finding(
                        id='T001',
                        name='tx.origin usage',
                        severity='High',
                        description='Use of tx.origin for authorization is insecure; use msg.sender instead.',
                        file=filename,
                        line=line,
                        evidence='tx.origin used',
                        recommendation='Use msg.sender and proper access control patterns.'
                    )
                    findings.append(f.to_dict())
            for v in node.values():
                recurse(v)
        elif isinstance(node, list):
            for e in node:
                recurse(e)

    recurse(ast)
    return findings

