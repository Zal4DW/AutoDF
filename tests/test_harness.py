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


def test_click_runs_bundled_script():
    out = cmds(["click", "Work orders", "-n", "2"])
    assert out[:2] == ["lua", "-f"]
    assert out[2].endswith("autodf/lua/click.lua") and "\\" not in out[2]
    assert os.path.exists(out[2])
    assert out[3:] == ["text", "Work orders", "2"]


def test_clickat_report_director():
    assert cmds(["clickat", "29", "24"])[3:] == ["cell", "29", "24"]
    assert cmds(["report"])[2].endswith("report.lua")
    assert cmds(["mood"])[2].endswith("mood.lua") and os.path.exists(cmds(["mood"])[2])
    assert cmds(["director", "stop"])[3:] == ["stop"]


def test_run_sets_pause_timer():
    code = cmds(["run", "1200"])[1]
    assert "dfhack.timeout(1200,'ticks'" in code and "pause_state=false" in code


def test_decode_mixed_encodings():
    utf8 = "Kilrudsanád".encode("utf-8")
    cp437 = "Rigòth".encode("cp437")
    assert harness.decode(utf8 + b"\n" + cp437) == "Kilrudsanád\nRigòth"


def test_missing_binary(monkeypatch):
    monkeypatch.setenv("DFHACK_RUN", "/nonexistent/dfhack-run")
    code, out = harness.run_dfhack(["ls"])
    assert code == 127 and "not found" in out
