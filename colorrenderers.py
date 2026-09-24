from renderers import IRenderer

class ColorConsoleRenderer(IRenderer):
    def __init__(self):
        self.environment_statebuffer = None

    def observe(self, statebuffer):
        self.environment_statebuffer = statebuffer

    def render(self):
        state = self.environment_statebuffer.get_state()
        if not state:
            return

        width = state["width"]
        height = state["height"]
        location_colors = state["location_colors"]
        agents_locations = state["agents_locations"]
        agents_colors = state["agents_colors"]
        active_trails = state["active_trails"]

        trail_letter = {}
        for agent_id, trail in active_trails.items():
            letter = agents_colors.get(agent_id, "?")[0].lower()
            for cell in trail:
                trail_letter[cell] = letter

        header = "      " + " ".join(str(x % 10) for x in range(width))   # x de cada columna
        print(header)

        for y in range(height - 1, -1, -1):        # y de cada fila
            row = []
            for x in range(width):
                loc = (x, y)
                if loc in trail_letter:
                    row.append(trail_letter[loc])
                else:
                    color = location_colors.get(loc, "none")
                    row.append(color[0].upper() if color != "none" else ".")
            print(f"y={y:<3}" + " ".join(row))

        for agent_id, loc in agents_locations.items():
            print(f"  Agente {agent_id}: color={agents_colors.get(agent_id)}, posición={loc}")
        print()