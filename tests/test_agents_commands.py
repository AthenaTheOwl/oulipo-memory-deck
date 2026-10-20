"""Every command and path AGENTS.md tells an agent to use must exist."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

from oulipo_memory_deck.cli import _build_parser

ROOT = Path(__file__).resolve().parents[1]
AGENTS = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
FENCE = re.compile(r"```(?:bash|sh)\n(.*?)```", re.S)
COMMANDS = [
    line.strip()
    for block in FENCE.findall(AGENTS)
    for line in block.splitlines()
    if line.strip() and not line.strip().startswith("#")
]
# paths named in the prose, e.g. `oulipo_memory_deck/swap.py`; the closing
# paragraph lists the scripts that do not exist, so skip that sentence
PROSE = AGENTS.split("There is no ")[0]
PATHS = re.findall(r"`((?:scripts|oulipo_memory_deck|dictionaries|cards|schemas)/[^`*\s]+)`", PROSE)


def test_agents_md_lists_runnable_gates() -> None:
    assert "python -m oulipo_memory_deck validate" in COMMANDS
    for command in COMMANDS:
        script = re.match(r"python3? (\S+\.py)\b", command)
        module = re.match(r"python3? -m oulipo_memory_deck (\S+)", command)
        if script:
            assert (ROOT / script.group(1)).is_file(), command
        elif module:
            # argparse exits on an unknown subcommand
            assert _build_parser().parse_args(command.split()[3:]).cmd == module.group(1), command
        else:
            assert command == "uv run pytest", command


def test_paths_named_in_agents_md_exist() -> None:
    assert "oulipo_memory_deck/swap.py" in PATHS
    missing = [path for path in PATHS if not (ROOT / path).exists()]
    assert missing == []


def test_agents_md_gate_commands_exit_zero() -> None:
    for command in COMMANDS:
        if command == "uv run pytest":
            continue  # this test already runs under pytest
        args = [sys.executable, *command.split()[1:]]
        completed = subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False)
        assert completed.returncode == 0, (command, completed.stdout, completed.stderr)
