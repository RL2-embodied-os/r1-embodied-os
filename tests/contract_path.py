"""Compatibility exports for tests; runtime code uses week01_contracts."""

from week01_contracts import (
    CONTRACTS_DIR,
    EXAMPLES_DIR,
    INTERFACES_DIR,
    WEEK01_ROOT,
    activate_contract_imports,
    require_contract_baseline,
)


__all__ = [
    "CONTRACTS_DIR",
    "EXAMPLES_DIR",
    "INTERFACES_DIR",
    "WEEK01_ROOT",
    "activate_contract_imports",
    "require_contract_baseline",
]
