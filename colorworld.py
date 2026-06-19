from statebuffer import IStateBuffer
from environments import SimulatedEnvironment

class ColorWorldEnvironment(SimulatedEnvironment):
    def __new__(cls, width: int, height: int):
        if width <= 0 or height <= 0:
            raise ValueError
        else:
            return super().__new__(cls)

    def __init__(self, width: int, height: int):
        super(ColorWorldEnvironment, self).__init__()
        self._width = width
        self._height = height
        self._agents_colors = {}                #maps agent id with its color
        self._agents_locations = {}             #maps agent id with its location (x, y)
        self._location_colors = {}              #maps location with the color present in that location

    def add(self, agent_id: int) -> None:
        super(ColorWorldEnvironment, self).add(agent_id)
        self._agents_locations[agent_id] = (0, 0)
        self._agents_colors[agent_id] = ""
    
    def remove(self, agent_id: int) -> None:
        super(ColorWorldEnvironment, self).remove(agent_id)
        self._agents_locations.pop(agent_id, None)
        self._agents_colors.pop(agent_id, None)

    def add_statebuffer(self, agent_id: int, statebuffer: IStateBuffer) -> None:
        super(ColorWorldEnvironment, self).add_statebuffer(agent_id, statebuffer)
        statebuffer.update({"width": self._width, 
                            "height": self._height, 
                            "agent_location": self._agents_locations.get(agent_id)
                            })

    def remove_statebuffer(self, agent_id: int,statebuffer: IStateBuffer) -> None:
        super(ColorWorldEnvironment, self).remove_statebuffer(agent_id, statebuffer)

    def _location_of(self, agent_id: int) -> tuple:
        return self._agents_locations[agent_id] if agent_id in self._agents_locations else None
    
    def _location_color(self, location: tuple) -> str:
        return self._location_colors.get(location, "none")
    
    def is_color_in_location(self, location: tuple, color: str) -> bool:
        return self._location_color(location) == color
    
    def _get_local_grid(self, agent_id: int) -> dict: #maps location color for a 10x10 grid centered around the agent
        x, y = self._location_of(agent_id)
        grid = {}
        for xi in range(-5, 5):
            for yi in range(-5, 5):
                location = (x + xi, y + yi)
                grid[location] = self._location_color(location)
        return grid

    def get_property(self, agent_id: int, property_name: str) -> dict:
        if agent_id in self._agents:
            response = {"agent": agent_id}

            property_methods = {
                "location": self._location_of,
                "local_grid": self._get_local_grid,
            }

            property_method = property_methods.get(property_name)

            if property_method:
                response[property_name] = property_method(agent_id)

            return response
        else:
            raise ValueError("Agent with id {} not found in the environment.".format(agent_id))    

    def _paint_location(self, agent_id: int) -> None:
        location = self._location_of(agent_id)
        if 0 <= location[0] < self._width and 0 <= location[1] < self._height:
            self._location_colors[location] = self._agents_colors.get(agent_id)

    def _handle_move(self, agent_id: int, direction: str) -> None:
        if direction == "left":
            self._move_agent_left(agent_id)
        elif direction == "right":
            self._move_agent_right(agent_id)
        elif direction == "up":
            self._move_agent_up(agent_id)
        elif direction == "down":
            self._move_agent_down(agent_id)
        else:
            print(f"Invalid direction: {direction}")

    def _move_agent_left(self, agent_id: int):
        current_location = self._location_of(agent_id)
        new_location = (max(current_location[0] - 1, 0), current_location[1])
        self._agents_locations[agent_id] = new_location

    def _move_agent_right(self, agent_id: int):
        current_location = self._location_of(agent_id)
        new_location = (min(current_location[0] + 1, self._width - 1), current_location[1])
        self._agents_locations[agent_id] = new_location

    def _move_agent_up(self, agent_id: int):
        current_location = self._location_of(agent_id)
        new_location = (current_location[0], min(current_location[1] + 1, self._height - 1))
        self._agents_locations[agent_id] = new_location

    def _move_agent_down(self, agent_id: int):
        current_location = self._location_of(agent_id)
        new_location = (current_location[0], max(current_location[1] - 1, 0))
        self._agents_locations[agent_id] = new_location

    def take_action(self, agent_id: int, action_name: str, params: dict = {}) -> None:
        if agent_id in self._agents:
            action_methods = {
                "move": (self._handle_move, ["direction"]),
                "paint": (self._paint_location, []),
            }

            action_method, expected_params = action_methods.get(action_name, (None, None))
            if action_method:
                args = [agent_id] + [params.get(param) for param in expected_params]
                action_method(*args)
                self._update_statebuffers(agent_id)
            else:
                print(f"Invalid action: {action_name}")
        else:
            raise ValueError("Agent with id {} not found in the environment.".format(agent_id))
    
    def _update_statebuffers(self, agent_id: int) -> None:
        relevant_statebuffers = [entry["statebuffer"] for entry in self._statebuffers if entry["agent_id"] == agent_id]
        for statebuffer in relevant_statebuffers:
            statebuffer.update({"height": self._height, "width": self._width, "agent_location": self._location_of(agent_id),
                             "agent_color": self._agents_colors.get(agent_id), "location_color": self._location_color(self._location_of(agent_id))})
