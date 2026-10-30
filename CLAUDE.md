# Playing Dwarf Fortress with AutoDF

You are the player. Drive a running Dwarf Fortress (with DFHack) using the harness:

    python -m autodf status            # year/tick/pause/citizen count
    python -m autodf screen            # read what is on screen
    python -m autodf keys D_DESIGNATE  # send interface keys (see DF keybinding names)
    python -m autodf cmd "autochop status"   # any DFHack command
    python -m autodf lua "print(#df.global.world.units.active)"
    python -m autodf pause | unpause
    python -m autodf announcements -n 20

Set `DFHACK_RUN` to the full path of `dfhack-run` if it is not on PATH.

Loop: `status` -> `screen`/`announcements` -> act -> repeat. Pause before
making complex changes. Priorities: food, drink, shelter, then industry and
defense. Prefer DFHack automation (autofarm, autochop, buildingplan, quickfort)
over many individual keypresses.
