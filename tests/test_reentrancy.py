from auditor.parser import parse_file
from auditor.detectors.reentrancy import find_reentrancy


def test_vulnerable_contract_detected(tmp_path):
    p = tmp_path / "vul.sol"
    p.write_text('''// SPDX-License-Identifier: MIT\npragma solidity ^0.6.0;\ncontract C{mapping(address=>uint) balances; function withdraw(){(bool s,)=msg.sender.call(""); balances[msg.sender]-=1;}}''')
    ast = parse_file(str(p))
    findings = find_reentrancy(ast, str(p))
    assert len(findings) >= 1

