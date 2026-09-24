from colorworld import ColorWorldEnvironment
from statebuffer import StateBuffer
from colorrenderers import ColorConsoleRenderer
 
env = ColorWorldEnvironment(width=14, height=6)
env.add(1, color="red", coords=(2, 2))
env.add(2, color="blue", coords=(10, 2))
 
statebuffer = StateBuffer(0, env)
renderer = ColorConsoleRenderer()
renderer.observe(statebuffer)
 
renderer.render()
 
pasos = [
    (1, "right"), (1, "right"), (1, "right"), (1, "down"),
    (2, "left"), (2, "left"), (2, "left"), (2, "left"), (2, "left"),
]
 
for agente_id, direccion in pasos:
    env.take_action(agente_id, "move", {"direction": direccion})
    renderer.render()
 
assert 1 not in env._agents
assert 2 in env._agents
print("Agente 1 eliminado por pisarle el rastro activo")