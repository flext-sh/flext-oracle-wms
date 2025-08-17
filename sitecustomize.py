# Test helper shim: provide a builtin `_run` for async subprocess execution
# This allows tests to call `_run(...)` even when not defined in the test scope.
from __future__ import annotations

import asyncio
import builtins


async def _run(cmd_list: list[str], cwd: str | None = None) -> tuple[int, str, str]:
    proc = await asyncio.create_subprocess_exec(
      *cmd_list,
      cwd=cwd,
      stdout=asyncio.subprocess.PIPE,
      stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    return proc.returncode, stdout.decode(), stderr.decode()


# Expose as builtin so unqualified `_run` resolves when tests reference it
builtins._run = _run  # type: ignore[attr-defined]
