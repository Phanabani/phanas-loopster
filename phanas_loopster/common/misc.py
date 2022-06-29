__all__ = ["flatten", "pathstr"]

from collections.abc import Iterable
from pathlib import Path
from typing import TypeVar

T = TypeVar("T")


def flatten(iterable: Iterable[T]) -> list[T]:
    out = []
    for x in iterable:
        if isinstance(x, Iterable) and not isinstance(x, str):
            for y in x:
                out.append(y)
        else:
            out.append(x)
    return out


def pathstr(path: Path) -> str:
    return str(path.expanduser().resolve().absolute())
