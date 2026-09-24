from colorworld import ColorWorldEnvironment
from statebuffer import StateBuffer
from colorrenderers import ColorConsoleRenderer
 
env = ColorWorldEnvironment(width=10, height=6)
env.add(1, color="red", coords=(2, 2))
env.add(2, color="blue", coords=(6, 2))
 
statebuffer = StateBuffer(0, env)
renderer = ColorConsoleRenderer()
renderer.observe(statebuffer)
 
renderer.render()
 
pasos = ["right", "right", "right", "right"]
 
for direccion in pasos:
    env.take_action(1, "move", {"direction": direccion})
    renderer.render()
 
assert 1 not in env._agents
assert 2 in env._agents
print("Agente 1 eliminado por pisar la celda donde ya estaba parado Agente 2")
 