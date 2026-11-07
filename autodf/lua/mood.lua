-- Mood report: each dwarf's stress, unmet needs and strongest recent thoughts,
-- then a fortress-wide count of the most common thoughts.
-- Stress below 0 is content; above about 25,000 a dwarf is unhappy and at risk.
local tally = {}
for _, u in ipairs(dfhack.units.getCitizens()) do
  local p = u.status.current_soul.personality
  local unmet = {}
  for _, n in ipairs(p.needs) do
    if n.focus_level < -999 then
      unmet[#unmet + 1] = df.need_type[n.id] .. '(' .. n.focus_level .. ')'
    end
  end
  local thoughts = {}
  for i = #p.emotions - 1, math.max(0, #p.emotions - 6), -1 do
    local e = p.emotions[i]
    local name = df.unit_thought_type[e.thought] or tostring(e.thought)
    local feel = df.emotion_type[e.type] or tostring(e.type)
    thoughts[#thoughts + 1] = feel .. ':' .. name
  end
  for _, e in ipairs(p.emotions) do
    local name = df.unit_thought_type[e.thought] or tostring(e.thought)
    tally[name] = (tally[name] or 0) + 1
  end
  print(('%-20s stress %7d'):format(dfhack.units.getProfessionName(u), p.stress))
  if #unmet > 0 then print('  unmet: ' .. table.concat(unmet, ' ')) end
  print('  recent: ' .. table.concat(thoughts, ', '))
end
local list = {}
for k, v in pairs(tally) do list[#list + 1] = {k, v} end
table.sort(list, function(a, b) return a[2] > b[2] end)
local top = {}
for i = 1, math.min(12, #list) do top[#top + 1] = list[i][1] .. ' x' .. list[i][2] end
print('common thoughts: ' .. table.concat(top, ', '))
