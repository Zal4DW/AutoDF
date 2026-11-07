-- Fortress report: each dwarf's job and position, digging left per z-level, key stocks,
-- active work orders, and the last few announcements.
for _, u in ipairs(dfhack.units.getCitizens()) do
  local job = u.job.current_job and dfhack.job.getName(u.job.current_job) or 'idle'
  print(('%-18s %-30s %d,%d,%d'):format(dfhack.units.getProfessionName(u), job, u.pos.x, u.pos.y, u.pos.z))
end

local dig = {}
for _, blk in ipairs(df.global.world.map.map_blocks) do
  for x = 0, 15 do for y = 0, 15 do
    if blk.designation[x][y].dig ~= df.tile_dig_designation.No then
      dig[blk.map_pos.z] = (dig[blk.map_pos.z] or 0) + 1
    end
  end end
end
local zs = {}
for z in pairs(dig) do zs[#zs + 1] = z end
table.sort(zs, function(a, b) return a > b end)
local parts = {}
for _, z in ipairs(zs) do parts[#parts + 1] = z .. ':' .. dig[z] end
print('dig left by z: ' .. (#parts > 0 and table.concat(parts, ' ') or 'none'))

local cnt = {}
for _, i in ipairs(df.global.world.items.other.IN_PLAY) do
  local t = df.item_type[i:getType()]
  cnt[t] = (cnt[t] or 0) + i:getStackSize()
end
print(('stocks: meat %d fish %d plant %d seeds %d drink %d logs %d boulders %d blocks %d'):format(
  cnt.MEAT or 0, cnt.FISH or 0, cnt.PLANT or 0, cnt.SEEDS or 0, cnt.DRINK or 0,
  cnt.WOOD or 0, cnt.BOULDER or 0, cnt.BLOCKS or 0))

local open = 0
for _, o in ipairs(df.global.world.manager_orders.all) do
  if o.amount_left > 0 then open = open + 1 end
end
print(('work orders open: %d (manager timer %d)'):format(open, df.global.plotinfo.manager_timer))

local r = df.global.world.status.reports
for i = math.max(0, #r - 8), #r - 1 do print('> ' .. r[i].text) end
