from __future__ import annotations

__all__ = ["run"]

from collections.abc import Iterable
import subprocess
from subprocess import CompletedProcess, PIPE

from phanas_loopster.common.misc import flatten


def run(*args: str | Iterable[str]) -> CompletedProcess[str]:
    proc = subprocess.run(flatten(args), stdout=PIPE, stderr=PIPE, encoding="utf_8")
    proc.check_returncode()
    return proc
