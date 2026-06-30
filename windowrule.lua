local size = { 100, 100 } -- x, y
hl.window_rule({
  name = "LCH",
  match = {
    class = "LCH",
  },
  float = true,
  size = size,
  min_size = size,
  center = true,
  border_size = 0,
  dim_around = true,
  no_shadow = true,
  stay_focused = true,
})
