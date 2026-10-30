-- Left-click on-screen text, or a screen cell.
--   click.lua text <text> [occurrence]
--   click.lua cell <x> <y>
-- Moves DF's own mouse and sends the click through DFHack, so the game window
-- does not need focus. DF ignores instant OS clicks; this path avoids that too.
local mode, a, b = ...

local function click(x, y)
  local gps = df.global.gps
  gps.mouse_x, gps.mouse_y = x, y
  gps.precise_mouse_x = x * gps.tile_pixel_x + 4
  gps.precise_mouse_y = y * gps.tile_pixel_y + 4
  require('gui').simulateInput(dfhack.gui.getCurViewscreen(true), '_MOUSE_L')
end

if mode == 'cell' then
  click(tonumber(a), tonumber(b))
  print(('clicked cell %s,%s'):format(a, b))
  return
end

local text, nth = a, tonumber(b) or 1
local w, h = dfhack.screen.getWindowSize()
local found = 0
for y = 0, h - 1 do
  local t = {}
  for x = 0, w - 1 do
    local p = dfhack.screen.readTile(x, y)
    t[#t + 1] = (p and p.ch and p.ch >= 32 and p.ch < 127) and string.char(p.ch) or ' '
  end
  local line, s = table.concat(t), 1
  while true do
    local i = line:find(text, s, true)
    if not i then break end
    found = found + 1
    if found == nth then
      local x = i - 1 + math.floor(#text / 2)
      click(x, y)
      print(('clicked "%s" at %d,%d'):format(text, x, y))
      return
    end
    s = i + 1
  end
end
qerror(('text not on screen: "%s" (found %d of %d)'):format(text, found, nth))
