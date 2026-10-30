-- On an open trade screen: select merchant goods by item type, select all of our goods,
-- and print both totals. Nothing is traded until the Trade button is pressed.
--   trade_select.lua MEAT FISH CHEESE ...   (item types to buy; BARREL buys only drink-filled barrels)
local t = df.global.game.main_interface.trade
if not t.open then qerror('trade screen is not open') end
local want = {}
for _, name in ipairs({...}) do want[name] = true end

local function contents(it)
  local out = {}
  for _, ref in ipairs(it.general_refs) do
    if ref:getType() == df.general_ref_type.CONTAINS_ITEM then out[#out + 1] = df.item.find(ref.item_id) end
  end
  return out
end

local buy, n = 0, 0
for i, it in ipairs(t.good[0]) do
  local name = df.item_type[it:getType()]
  local ok = want[name]
  if ok and name == 'BARREL' then
    local c = contents(it)
    ok = #c > 0 and c[1]:getType() == df.item_type.DRINK
  end
  t.goodflag[0][i].selected = ok and true or false
  if ok then
    buy = buy + dfhack.items.getValue(it)
    n = n + 1
  end
end

local sell = 0
for i, it in ipairs(t.good[1]) do
  t.goodflag[1][i].selected = true
  sell = sell + dfhack.items.getValue(it)
end
print(('buying %d items worth %d; offering %d items worth %d'):format(n, buy, #t.good[1], sell))
