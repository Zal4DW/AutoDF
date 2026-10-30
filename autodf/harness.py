"""Thin wrapper around DFHack's ``dfhack-run`` so an agent can play Dwarf Fortress.

Configure with env vars:
  DFHACK_RUN  path to the dfhack-run executable (default: ``dfhack-run`` on PATH)
"""
import argparse
import os
import shlex
import subprocess
import sys

SCREEN_LUA = (
    "local w,h=dfhack.screen.getWindowSize();"
    "for y=0,h-1 do local t={} for x=0,w-1 do "
    "local p=dfhack.screen.readTile(x,y);"
    "local c=(p and p.ch and p.ch>=32) and dfhack.df2utf(string.char(p.ch)) or ' ';"
    "t[#t+1]=c end print((table.concat(t):gsub('%s+$',''))) end"
)


def dfhack_binary():
    return os.environ.get("DFHACK_RUN", "dfhack-run")


def run_dfhack(args, timeout=60):
    """Run a dfhack-run command; returns (exit_code, combined output)."""
    try:
        proc = subprocess.run(
            [dfhack_binary(), *args],
            capture_output=True, text=True, timeout=timeout,
        )
    except FileNotFoundError:
        return 127, f"{dfhack_binary()} not found; set DFHACK_RUN to its path"
    except subprocess.TimeoutExpired:
        return 124, "dfhack-run timed out"
    return proc.returncode, (proc.stdout + proc.stderr).strip()


def lua_string(s):
    return "[=[" + s.replace("]=]", "]=].. ']=]' ..[=[") + "]=]"


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
    raise ValueError(a)


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
    return p


def main(argv=None):
    args = parser().parse_args(argv)
    code, out = run_dfhack(build_commands(args))
    if out:
        print(out)
    return code


if __name__ == "__main__":
    sys.exit(main())
