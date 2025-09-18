from auditor.parser import parse_file
from auditor.detectors.integer_overflow import find_integer_overflow


def test_overflow_detected(tmp_path):
    p = tmp_path / "vul2.sol"
    p.write_text('''// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;
contract C{function f(uint x){uint y = x + 1;}}''')
    ast = parse_file(str(p))
    findings = find_integer_overflow(ast, str(p))
    assert len(findings) >= 1

