import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from autodf import harness


def cmds(argv):
    return harness.build_commands(harness.parser().parse_args(argv))


def test_cmd_split():
    assert cmds(["cmd", "autochop status"]) == ["autochop", "status"]


def test_keys():
    out = cmds(["keys", "LEAVESCREEN", "SELECT"])
    assert out[0] == "lua" and "[=[SELECT]=]" in out[1]


def test_pause_and_status():
    assert "pause_state=true" in cmds(["pause"])[1]
    assert "citizens" in cmds(["status"])[1]


def test_missing_binary(monkeypatch):
    monkeypatch.setenv("DFHACK_RUN", "/nonexistent/dfhack-run")
    code, out = harness.run_dfhack(["ls"])
    assert code == 127 and "not found" in out
