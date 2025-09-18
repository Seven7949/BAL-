from solidity_parser import parser
import re


def parse_file(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        src = f.read()
    try:
        return parser.parse(src)
    except Exception:
        # Fallback: normalize Solidity 0.6+ call options syntax `.call{...}()`
        # into older-compatible `.call()` so the legacy parser can handle it.
        normalized = re.sub(r"\.call\s*\{[^}]*\}", ".call", src)
        return parser.parse(normalized)

