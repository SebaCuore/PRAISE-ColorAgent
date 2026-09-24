import time
from colorworld import ColorWorldEnvironment
from coloragent import ColorAgent
from statebuffer import StateBuffer
from colorrenderers import ColorConsoleRenderer

env = ColorWorldEnvironment(width=15, height=10)

agent1 = ColorAgent(env, color="red", spawn_coords=(2, 2))
agent2 = ColorAgent(env, color="blue", spawn_coords=(12, 7))
agent3 = ColorAgent(env, color="green", spawn_coords=(7, 5))
agent4 = ColorAgent(env, color="yellow", spawn_coords=(5, 8))

agents = {agent1.id: agent1, agent2.id: agent2, agent3.id: agent3, agent4.id: agent4}
alive = set(agents.keys())

statebuffer = StateBuffer(agent1.id, env)
renderer = ColorConsoleRenderer()
renderer.observe(statebuffer)

print("=== Estado inicial ===")
renderer.render()

for turn in range(30):
    print(f"--- Turno {turn + 1} ---")
    for agent_id in list(alive):
        try:
            agents[agent_id].behave()
        except ValueError:
            print(f"  Agente {agent_id} fue eliminado.")
            alive.discard(agent_id)
    renderer.render()
    time.sleep(0.3)

    if len(alive) <= 1:
        print("=== Partida terminada ===")
        break