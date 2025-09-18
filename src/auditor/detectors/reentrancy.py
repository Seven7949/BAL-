from .base import Finding

# Heuristic reentrancy detector
EXTERNAL_CALL_MEMBERS = {"call", "delegatecall", "transfer", "send"}


def _is_external_call_stmt(stmt):
    try:
        # Pattern 1: direct expression statement calling .call/.transfer/...
        if stmt.get('type') == 'ExpressionStatement':
            expr = stmt['expression']
            if expr['type'] == 'FunctionCall':
                callee = expr['expression']
                if callee['type'] == 'MemberAccess':
                    member = callee.get('memberName')
                    if member in EXTERNAL_CALL_MEMBERS:
                        return True, stmt
        # Pattern 2: declaration with initialValue invoking external call
        if stmt.get('type') == 'VariableDeclarationStatement':
            init = stmt.get('initialValue')
            if init and init.get('type') == 'FunctionCall':
                callee = init.get('expression')
                if callee and callee.get('type') == 'MemberAccess':
                    member = callee.get('memberName')
                    if member in EXTERNAL_CALL_MEMBERS:
                        return True, stmt
    except Exception:
        pass
    return False, None


def _is_state_write_stmt(stmt, state_vars):
    try:
        if stmt.get('type') == 'ExpressionStatement':
            expr = stmt.get('expression', {})
            # Pattern A: explicit Assignment
            if expr.get('type') == 'Assignment':
                left = expr.get('left', {})
                # left may be Identifier, MemberAccess, IndexAccess
                if left.get('type') == 'Identifier' and left.get('name') in state_vars:
                    return True
                if left.get('type') == 'MemberAccess':
                    base = left.get('expression')
                    if base and base.get('type') == 'Identifier' and base.get('name') in state_vars:
                        return True
                if left.get('type') == 'IndexAccess':
                    base = left.get('base')
                    if base and base.get('type') == 'Identifier' and base.get('name') in state_vars:
                        return True
            # Pattern B: compound assignment represented as BinaryOperation (e.g., -=)
            if expr.get('type') == 'BinaryOperation' and expr.get('operator') in {'+=', '-=', '*=', '/=', '%='}:
                left = expr.get('left', {})
                if left.get('type') == 'Identifier' and left.get('name') in state_vars:
                    return True
                if left.get('type') == 'MemberAccess':
                    base = left.get('expression')
                    if base and base.get('type') == 'Identifier' and base.get('name') in state_vars:
                        return True
                if left.get('type') == 'IndexAccess':
                    base = left.get('base')
                    if base and base.get('type') == 'Identifier' and base.get('name') in state_vars:
                        return True
    except Exception:
        pass
    return False


def find_reentrancy(ast, filename="<input>"):
    findings = []
    # gather state vars per contract
    for node in ast.get('children', []):
        if node.get('type') != 'ContractDefinition':
            continue
        state_vars = set()
        for sub in node.get('subNodes', []):
            if sub.get('type') == 'StateVariableDeclaration':
                for v in sub.get('variables', []):
                    state_vars.add(v.get('name'))

        # functions
        for sub in node.get('subNodes', []):
            if sub.get('type') == 'FunctionDefinition' and sub.get('body'):
                # Recursively flatten statements to capture nested blocks/ifs
                def flatten_statements(container):
                    result = []
                    if not container:
                        return result
                    # container could be a Block or a list of statements or a single statement
                    if isinstance(container, list):
                        items = container
                    else:
                        if container.get('type') == 'Block':
                            items = container.get('statements', [])
                        else:
                            items = [container]
                    for st in items:
                        st_type = st.get('type')
                        if st_type in {'ExpressionStatement', 'VariableDeclarationStatement'}:
                            result.append(st)
                        elif st_type == 'IfStatement':
                            # include inside TrueBody / FalseBody
                            result.extend(flatten_statements(st.get('TrueBody')))
                            false_body = st.get('FalseBody')
                            if false_body:
                                result.extend(flatten_statements(false_body))
                        elif st_type in {'ForStatement', 'WhileStatement', 'DoWhileStatement'}:
                            # conservatively include their bodies
                            result.extend(flatten_statements(st.get('body')))
                        elif st_type == 'ReturnStatement':
                            result.append(st)
                        elif st_type == 'Block':
                            result.extend(flatten_statements(st))
                        # else: skip other control flow types for MVP
                    return result

                stmts = flatten_statements(sub.get('body'))
                for i, stmt in enumerate(stmts):
                    is_call, call_node = _is_external_call_stmt(stmt)
                    if is_call:
                        # if any later stmt writes state -> suspicious
                        later_write = any(_is_state_write_stmt(s, state_vars) for s in stmts[i+1:])
                        if later_write:
                            line = stmt.get('loc', {}).get('start', {}).get('line', -1)
                            f = Finding(
                                id="R001",
                                name="Potential Reentrancy",
                                severity="High",
                                description="External call followed by state modification (checks-effects-interactions not followed).",
                                file=filename,
                                line=line,
                                evidence="External call before state write",
                                recommendation="Use checks-effects-interactions or a reentrancy guard (nonReentrant)."
                            )
                            findings.append(f.to_dict())
    return findings

