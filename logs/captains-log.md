# Captain's log: Kilrudzanád, "Bronzemorning"

World: the Continent of Glowing. Embark at world tile (48,87), temperate shrubland.
Fortress centre (Dreamfort central stairs): 134,44,163.

## Year 100, 15th Granite: embark

Seven dwarves arrived with the default "Play now" loadout. I scored all 3,572 usable land
tiles and took the best one on offer: a river, volcanism at 100, very deep soil, iron and
flux for steel. The world is harsh. Only 18 tiles counted as good-aligned, so this site is
neutral. A hostile goblin civilisation is two days' travel north-east.

The ground is easy. Four soil layers sit on solid stone from z158. The light aquifer is a
single layer at z160. I picked a 53x53 patch of flat ground 90 tiles north-east of the wagon
for the fortress, and the plan is DFHack's Dreamfort blueprint set.

## 15th–30th Granite: stairs, vents, first stall

- Turned on the Dreamfort automation set: autochop, autofarm, autofish, autobutcher,
  nestboxes, seedwatch, suspendmanager, tailor, prioritize and others.
- Applied /surface1 and /central_stairs, then designated the whole underground fortress
  (/dig_all, 5,418 tiles) with industry at z157.
- The aquifer cancelled the stair dig twice ("damp stone located"). I re-designated the
  four tiles by hand, and the stairs reached z157.
- Applied /surface2: four workshops, a trade depot, starter stockpiles and miasma vents.

## Slate: the long idle

Five dwarves stood in the meeting hall for two weeks. Three separate causes:

1. Buildingplan was set to blocks only, and nobody can make blocks without a mason's
   workshop. Re-placing the buildings with logs allowed fixed it.
2. Extra miners had the labour but never collected picks. Handing them a pick fixed it.
3. No work order ever became a job. I had appointed the manager from Lua, and the game
   listed them but didn't count them ("A manager is required to coordinate work orders").
   Appointing Rigòth through the nobles screen fixed it at once.

## Felsite: farms and drink

- Dug and built the farming level (/farming2): 9 plots, a still, kitchen, butcher,
  tanner, fishery and farmer's workshop. Plump helmets are planted.
- Imported the basic order set. Brewing stalled because its condition wanted more than
  5 empty containers and we had exactly 5. I lowered it to 1 and queued 5 barrels.
  Drink went from 40 to 65 in four days.
- Took every other labour off the two miners, and the industry level is moving again.

**State at 21st Felsite (tick 92,337):** 7 dwarves, food ~50, drink 65, 6 beds, all
surface and farm workshops built, industry level 725 tiles left to dig.

## Late Felsite to Hematite: comfort, food and the first migrants

Mood report at the start: five of seven content, the mason mildly stressed. Complaints were
drinking without cups, eating without chairs, sleeping on grass, no bedroom, and no
place to pray.

- Ordered wooden mugs, tables, chairs and beds so nothing waited on stone. All six
  tables and chairs are now built.
- Laid a temple and a tavern over the surface meeting hall (the tavern zone doubles as
  a dining hall). The tavern has no keeper yet.
- Made each of the seven beds a private bedroom and assigned them. Dwarves in this
  version do not claim rooms by themselves.
- Mixed the crops (cave wheat, sweet pods, plump helmets) after autofarm kept planting
  only plump helmets. Turned autofarm off.
- Brewing stalled on its empty-container rule; fixed. Drink went from 40 to about 160.
- Cooking stalled twice: lavish meals needed 4 ingredients, then Dreamfort's cooking
  ban covered every plant. Switched to easy meals and lifted the plant bans.
- Queued 20 rock crafts for the autumn caravan. The craftsdwarf's workshop was full of
  jobs nobody could do; bound the crafts order to it and raised its order limit.
- Planting moved off the crafters; miners now only mine.

**Migrants (mid-Hematite):** eight arrived, four of them children; population 15. Cut
the dig queue to the industry and services levels (everything from z152 down cancelled),
dug an 8x3 dormitory east of the bedrooms on the farm level and put 8 beds in it.
Marked 114 surface shrubs for gathering.

My cancel loop walked every map block and froze the game for about three minutes. It
recovered with no harm. Lesson recorded in CLAUDE.md.

**State at tick 179,337:** 15 dwarves, all with beds, ~31 meals, ~160 drink, stone
flowing (43 boulders, 60 blocks). Stress: the original seven are content except the
stoneworker (~10,900); the adult migrants are recovering; the four children are still
near 17,500.

## Next

- Finish digging the industry level, then /industry2 for permanent workshops and stone
  stockpiles. Stone jobs stay blocked until then.
- /surface3 to cover the vents and wall in the central stairs.
- Watch for the first migrant wave and the goblins.
