"""Resolve the contracts, examples, and interfaces inside this package."""

import sys
from pathlib import Path
from typing import Final


WEEK01_ROOT: Final[Path] = Path(__file__).resolve().parent
CONTRACTS_DIR: Final[Path] = WEEK01_ROOT / "contracts"
EXAMPLES_DIR: Final[Path] = WEEK01_ROOT / "examples"
INTERFACES_DIR: Final[Path] = WEEK01_ROOT / "interfaces"


def require_contract_baseline() -> Path:
    """Return the repository contract root or fail with an actionable message."""

    required = (CONTRACTS_DIR, EXAMPLES_DIR, INTERFACES_DIR)
    missing = [path for path in required if not path.is_dir()]
    if missing:
        rendered = ", ".join(str(path) for path in missing)
        raise RuntimeError(
            "The self-contained Week 1 contract baseline is incomplete. "
            f"Missing: {rendered}"
        )
    return WEEK01_ROOT


def activate_contract_imports() -> Path:
    """Expose this package's interface modules to the current process."""

    root = require_contract_baseline()
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    return root
