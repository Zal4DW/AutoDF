"""Thin wrapper around DFHack's ``dfhack-run`` so an agent can play Dwarf Fortress.

Configure with env vars:
  DFHACK_RUN  path to the dfhack-run executable (default: ``dfhack-run`` on PATH)
"""
import argparse
import os
import shlex
import subprocess
import sys
import time

LUA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lua")

SCREEN_LUA = (
    "local w,h=dfhack.screen.getWindowSize();"
    "for y=0,h-1 do local t={} for x=0,w-1 do "
    "local p=dfhack.screen.readTile(x,y);"
    "local c=(p and p.ch and p.ch>=32) and dfhack.df2utf(string.char(p.ch)) or ' ';"
    "t[#t+1]=c end print((table.concat(t):gsub('%s+$',''))) end"
)


def dfhack_binary():
    return os.environ.get("DFHACK_RUN", "dfhack-run")


def decode(data):
    """Decode dfhack-run output line by line.

    Screen text arrives as UTF-8, but unit and place names arrive in DF's CP437,
    so a line that is not valid UTF-8 is read as CP437.
    """
    lines = []
    for line in data.splitlines():
        try:
            lines.append(line.decode("utf-8"))
        except UnicodeDecodeError:
            lines.append(line.decode("cp437"))
    return "\n".join(lines)


def run_dfhack(args, timeout=60):
    """Run a dfhack-run command; returns (exit_code, combined output)."""
    try:
        proc = subprocess.run(
            [dfhack_binary(), *args],
            capture_output=True, timeout=timeout,
        )
    except FileNotFoundError:
        return 127, f"{dfhack_binary()} not found; set DFHACK_RUN to its path"
    except subprocess.TimeoutExpired:
        return 124, "dfhack-run timed out"
    return proc.returncode, decode(proc.stdout + proc.stderr).strip()


def lua_string(s):
    return "[=[" + s.replace("]=]", "]=].. ']=]' ..[=[") + "]=]"


def lua_script(name, *args):
    """dfhack-run argv that runs one of the bundled scripts in autodf/lua."""
    path = os.path.join(LUA_DIR, name + ".lua").replace("\\", "/")
    return ["lua", "-f", path, *[str(a) for a in args]]


def build_commands(args):
    """Translate a parsed CLI action into a dfhack-run argv list."""
    a = args.action
    if a == "cmd":
        return shlex.split(args.text)
    if a == "lua":
        return ["lua", args.code]
    if a == "keys":
        keys = ",".join(lua_string(k) for k in args.keys)
        code = (
            "local gui=require('gui');"
            f"for _,k in ipairs({{{keys}}}) do "
            "gui.simulateInput(dfhack.gui.getCurViewscreen(true), k) end"
        )
        return ["lua", code]
    if a == "screen":
        return ["lua", SCREEN_LUA]
    if a == "pause":
        return ["lua", "df.global.pause_state=true"]
    if a == "unpause":
        return ["lua", "df.global.pause_state=false"]
    if a == "status":
        return ["lua",
                "print('year',df.global.cur_year,'tick',df.global.cur_year_tick,"
                "'paused',df.global.pause_state);"
                "print('citizens',#dfhack.units.getCitizens())"]
    if a == "announcements":
        return ["lua",
                f"local r=df.global.world.status.announcements;"
                f"for i=math.max(0,#r-{args.count}),#r-1 do print(r[i].text) end"]
    if a == "click":
        return lua_script("click", "text", args.text, args.n)
    if a == "clickat":
        return lua_script("click", "cell", args.x, args.y)
    if a == "report":
        return lua_script("report")
    if a == "mood":
        return lua_script("mood")
    if a == "director":
        return lua_script("director", args.mode)
    if a == "run":
        return ["lua",
                f"dfhack.timeout({args.ticks},'ticks',function() df.global.pause_state=true end);"
                "df.global.pause_state=false"]
    raise ValueError(a)


def wait_for_pause(limit, poll=3.0):
    """Poll until the game pauses or `limit` seconds pass; returns True if it paused."""
    deadline = time.monotonic() + limit
    while time.monotonic() < deadline:
        time.sleep(poll)
        code, out = run_dfhack(["lua", "print(df.global.pause_state)"])
        if code == 0 and out.strip() == "true":
            return True
    return False


def parser():
    p = argparse.ArgumentParser(prog="autodf", description=__doc__)
    sub = p.add_subparsers(dest="action", required=True)
    c = sub.add_parser("cmd", help="run a DFHack console command")
    c.add_argument("text")
    l = sub.add_parser("lua", help="run Lua code inside DF")
    l.add_argument("code")
    k = sub.add_parser("keys", help="send interface keys, e.g. D_DESIGNATE LEAVESCREEN")
    k.add_argument("keys", nargs="+")
    sub.add_parser("screen", help="dump the current game screen as text")
    sub.add_parser("pause")
    sub.add_parser("unpause")
    sub.add_parser("status", help="year/tick/pause/citizen summary")
    n = sub.add_parser("announcements", help="recent game announcements")
    n.add_argument("-n", "--count", type=int, default=20)
    t = sub.add_parser("click", help="left-click on-screen text, e.g. Okay")
    t.add_argument("text")
    t.add_argument("-n", type=int, default=1, help="which occurrence to click")
    x = sub.add_parser("clickat", help="left-click a screen cell (columns, rows)")
    x.add_argument("x", type=int)
    x.add_argument("y", type=int)
    sub.add_parser("report", help="dwarves' jobs, digging left, stocks, orders, news")
    sub.add_parser("mood", help="each dwarf's stress, unmet needs and recent thoughts")
    d = sub.add_parser("director", help="camera follows dwarves doing visible work")
    d.add_argument("mode", choices=["start", "stop"])
    r = sub.add_parser("run", help="unpause for N ticks (1200 = one day), then wait for the pause")
    r.add_argument("ticks", type=int)
    r.add_argument("--timeout", type=float, default=600, help="seconds to wait (default 600)")
    return p


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    args = parser().parse_args(argv)
    code, out = run_dfhack(build_commands(args))
    if out:
        print(out)
    if args.action == "click" and "text not on screen" in out:
        return 1  # dfhack-run exits 0 even when the script raises qerror
    if args.action == "run" and code == 0:
        if not wait_for_pause(args.timeout):
            print(f"still running after {args.timeout:.0f}s")
            return 1
        code, out = run_dfhack(build_commands(parser().parse_args(["status"])))
        print(out)
    return code


if __name__ == "__main__":
    sys.exit(main())
