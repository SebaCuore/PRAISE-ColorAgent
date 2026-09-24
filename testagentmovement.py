from colorworld import ColorWorldEnvironment
from statebuffer import StateBuffer
from colorrenderers import ColorConsoleRenderer
 
env = ColorWorldEnvironment(width=12, height=10)
env.add(1, color="red", coords=(5, 5))
 
statebuffer = StateBuffer(0, env)
renderer = ColorConsoleRenderer()
renderer.observe(statebuffer)
 
renderer.render()
 
pasos = ["right", "right", "right", "up", "up", "up", "left", "left", "left", "down", "down"]
 
for direccion in pasos:
    env.take_action(1, "move", {"direction": direccion})
    renderer.render()
 
assert env._active_trails.get(1, []) == []
print("Rastro consolidado correctamente")
 