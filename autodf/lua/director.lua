-- Camera director: while the game runs, centre the view on a dwarf doing visible work.
--   director.lua start | stop
-- Re-arms itself every 250 ticks, so it only moves the camera while unpaused.
local mode = ... or 'start'
local SKIP = {DrinkItem=true, Eat=true, Sleep=true, StoreItemInStockpile=true, Rest=true}
local PREFER = {Dig=3, CarveDownwardStaircase=3, CarveUpwardStaircase=3, CarveUpDownStaircase=3,
  DigChannel=3, ConstructBuilding=4, FellTree=2}

if mode == 'stop' then
  dfhack.autodf_director = nil
  print('camera director stopped')
  return
end

local token = {}
dfhack.autodf_director = token -- a newer start replaces older loops
local last

local function pick()
  local best, best_score
  for _, u in ipairs(dfhack.units.getCitizens()) do
    local j = u.job.current_job
    if j and not SKIP[df.job_type[j.job_type]] then
      local s = (PREFER[df.job_type[j.job_type]] or 1) + (u.id == last and -2 or 0) + math.random()
      if not best_score or s > best_score then best, best_score = u, s end
    end
  end
  return best
end

local function tick()
  if dfhack.autodf_director ~= token then return end
  local u = pick()
  if u then
    last = u.id
    dfhack.gui.revealInDwarfmodeMap(u.pos, true, true)
  end
  dfhack.timeout(250, 'ticks', tick)
end

tick()
print('camera director running')
