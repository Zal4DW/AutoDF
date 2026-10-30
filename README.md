# AutoDF
Sandbox playing DF using AI.

`autodf` is a small harness (stdlib-only Python) wrapping DFHack's `dfhack-run`
so an agent such as Claude Code can play Dwarf Fortress autonomously. See
[CLAUDE.md](CLAUDE.md) for the commands and play loop. Tests: `pytest tests`.

Helper Lua scripts that run inside DF live in `autodf/lua/`: clicking on-screen text,
a fortress report, and a camera director that follows working dwarves so a person can
watch. `logs/captains-log.md` records the current fortress.
