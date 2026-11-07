-- Mark goods for the trade depot (haulers then carry them there).
--   trade.lua <item_type>[:<max>] ...     e.g. trade.lua FIGURINE RING CAGE:15 ROUGH
-- Skips forbidden items, items in buildings or jobs, and items someone is carrying.
-- Uses dfhack.items.markForTrade, the call behind DFHack's "Move goods" screen.
local depot = df.global.world.buildings.other.TRADE_DEPOT[0]
if not depot or depot:getBuildStage() < depot:getMaxBuildStage() then
  qerror('no finished trade depot')
end
local total, value = 0, 0
for _, spec in ipairs({...}) do
  local name, max = spec:match('^(%u+):?(%d*)$')
  max = tonumber(max) or math.huge
  local vec = df.global.world.items.other[name]
  if not vec then qerror('unknown item type ' .. spec) end
  local n = 0
  for _, i in ipairs(vec) do
    if n >= max then break end
    local f = i.flags
    if not (f.in_building or f.in_job or f.forbid or f.trader or f.in_inventory or f.removed)
        and not dfhack.items.getHolderUnit(i) and dfhack.items.markForTrade(i, depot) then
      n = n + 1
      value = value + dfhack.items.getValue(i)
    end
  end
  print(('%s: %d marked'):format(name, n))
  total = total + n
end
print(('marked %d items, value %d'):format(total, value))
