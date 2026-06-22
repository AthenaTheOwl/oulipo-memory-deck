"""S+7 transform — canonical module name.

The implementation lives in `swap.py`. This module re-exports the
public surface so callers can import either name. Tests and the
factory contract reference `transform`; the original v0 scaffold
used `swap`. Both names point at the same functions.
"""

from __future__ import annotations

from .swap import (
    load_dictionary,
    swap,
)

transform = swap

__all__ = ["load_dictionary", "swap", "transform"]
