# -1 because we are repeating, so the initial command counts as one
<user.ordinals>:
  core.repeat_command(ordinals-1)
  user.quick_action_set("core.repeat_command")
repeat that: core.repeat_command(1)
repeat that <number_small> [times]: core.repeat_command(number_small)

