# Playing Dwarf Fortress with AutoDF

You are the player. Drive a running Dwarf Fortress (with DFHack) using the harness:

    python -m autodf status            # year/tick/pause/citizen count
    python -m autodf report            # each dwarf's job, digging left per z, stocks, orders, news
    python -m autodf mood              # each dwarf's stress, unmet needs, recent thoughts
    python -m autodf screen            # read what is on screen
    python -m autodf keys D_DESIGNATE  # send interface keys (see DF keybinding names)
    python -m autodf click Okay        # click on-screen text (-n 2 for the 2nd match)
    python -m autodf clickat 29 24     # click a screen cell (columns, rows)
    python -m autodf cmd "autochop status"   # any DFHack command
    python -m autodf lua "print(#df.global.world.units.active)"
    python -m autodf run 1200          # unpause for 1200 ticks (one day), wait for the pause
    python -m autodf director start    # camera follows dwarves doing visible work
    python -m autodf pause | unpause
    python -m autodf announcements -n 20

On Windows use `py` if `python` opens the Microsoft Store. Set `DFHACK_RUN` to the
full path of `dfhack-run` if it is not on PATH. With the Steam version it is
`...\steamapps\common\DFHack\hack\dfhack-run.exe`, and DFHack only loads when the
game is started from the DFHack entry in the Steam library.

Loop: `report` -> act -> `run <ticks>` -> repeat. Pause before making complex changes.
Priorities: food, drink, shelter, then industry and defense. Prefer DFHack automation
(autofarm, autochop, buildingplan, quickfort) over many individual keypresses.

## Watching

The user watches the game window. Run `director start` once per session so the camera
moves to the work. Before an action at a known place, centre on it:
`lua "dfhack.gui.revealInDwarfmodeMap(xyz2pos(x,y,z), true, true)"`.

## Building the fortress

Use DFHack's Dreamfort blueprints. `cmd "quickfort run library/dreamfort.csv -n /checklist"`
prints the order of steps, and each `/..._help` section explains its level. Apply with
`cmd "quickfort run library/dreamfort.csv -n /surface1 -c x,y,z"` and try `--dry-run` first.
Keep the fortress centre in `logs/captains-log.md`.

## Known traps

- **Appoint nobles through the game screen, not Lua.** Writing the position from Lua
  shows the noble in the list, but the game does not count them and no work order ever
  becomes a job. Use `keys D_NOBLES`, then `clickat` the "+" on the row and click the
  dwarf. The Work orders tab says "A manager is required" when this is wrong.
- **Damp stone cancels digging.** Designations next to an aquifer are dropped with
  "damp stone located". Set them again by hand on the affected tiles.
- **Buildingplan "blocks only" deadlocks a new fort.** Nobody can make blocks before a
  mason's workshop exists. Keep `buildingplan set logs true` and `boulders true` until
  stone is flowing. A building keeps the filter it was placed with, so re-place stuck ones.
- **New miners may never collect a pick.** If a dwarf has the MINE labour but no pick,
  move a free pick into their inventory.
- **Stone orders need stone.** Rock blocks, doors and pots cancel with "needs
  non-economic hard stone boulders" until the miners reach a stone layer.
- **Order conditions can stall production.** Read `item_conditions` on an inactive order
  before assuming the order system is broken.
- **Never loop over the whole map while writing.** Lua runs on the game thread; a loop
  that edits every map block froze the game for three minutes. Bound loops to x/y/z
  ranges, or use quickfort to change designations.
- **Don't dig everything at once.** Dreamfort's `/dig_all` queues ~5,400 tiles over ten
  levels. Seven dwarves can't keep up; dig a level when it is next needed.
- **Labour focus.** Every dwarf starts with every labour, so planting and hauling soak up
  the crafters. Give miners MINE only, and keep PLANT on two or three dwarves.
- **Dreamfort's `ban-cooking all` starves the kitchen** once raw meat and fish run out:
  it bans cooking every brewable plant. Lift the Cook bans on PLANT and PLANT_GROWTH
  entries in `df.global.plotinfo.kitchen` (keep the SEEDS bans) when drink is plentiful.
- **autofarm overrides manual crop choices** and put every underground plot on plump
  helmets. Disable it and set `plant_id[0..3]` on each farm plot to mix crops.
- **A workshop takes at most 5 general orders.** Unworkable jobs (wrong stone) fill the
  slots and block new orders. Bind important orders to a workshop (`workshop_id`) and
  raise `profile.max_general_orders`.
- **Bedrooms are not claimed automatically.** Zone one bed per bedroom (quickfort merges
  neighbouring cells unless each has `(1x1)`), then `dfhack.buildings.setOwner(zone, unit)`.
- **Quickfort ignored `start()` offsets here.** The cursor is the top-left cell of each
  section; write blueprints that way.
- **Tavern keepers cannot be set from Lua safely.** The tavern works without one.
- DF ignores instant OS mouse clicks. `click`/`clickat` go through DFHack and avoid this.
- `io.write` output does not reach `dfhack-run`; use `print` in Lua.

## Repo blueprints and orders

`autodf/blueprints/morale.csv` (temple, tavern, bedrooms, dormitory, foraging) and
`autodf/orders/*.json` (wooden comforts, beds, trade goods). Copy them to
`<DF>/dfhack-config/blueprints/autodf/` and `<DF>/dfhack-config/orders/` (as
`autodf_<name>.json`), then `quickfort run autodf/morale.csv -n /<label> -c x,y,z` or
`orders import autodf_<name>`.
