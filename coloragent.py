from environments import SimulatedSensor, SimulatedActuator, SimulatedEnvironment
from agents import Agent
from random import randrange

class LocationSensor(SimulatedSensor):

    def sense(self):
        response = self._env.get_property(self._agent.id, property_name="location")
        return response["location"]


class LocalGridSensor(SimulatedSensor):

    def sense(self):
        response = self._env.get_property(self._agent.id, property_name="local_grid")
        return response["local_grid"]

from enum import Enum, unique

@unique
class MoveDirection(Enum):
    LEFT = 'left'
    RIGHT = 'right'
    UP = 'up'
    DOWN = 'down'

class MoverActuator(SimulatedActuator):
    
    def act(self, direction: MoveDirection = MoveDirection.RIGHT):
        request_info = {"direction": direction.value}
        self._env.take_action(self._agent.id, "move", request_info)

class ColorAgent(Agent):

    def function(self, percept):
        directions = [MoveDirection.RIGHT, MoveDirection.LEFT, MoveDirection.UP, MoveDirection.DOWN]
        choice = randrange(4)
        return {"name": "move", "params": {"direction": directions[choice]}}

    def __init__(self, env: SimulatedEnvironment, color: str = "red", spawn_coords: tuple = (0, 0)):
        super().__init__()
        self._color = color
        self._spawn_coords = spawn_coords
        env.add(self.id, color=self._color, coords=self._spawn_coords)

        mover = MoverActuator(env)
        mover.agent = self
        self.add_actuator("mover", mover)

        locator = LocationSensor(env)
        locator.agent = self
        self.add_sensor("location_sensor", locator)

        local_grid_sensor = LocalGridSensor(env)
        local_grid_sensor.agent = self
        self.add_sensor("local_grid_sensor", local_grid_sensor)

    def print_state(self):
        print("Estoy en la posición {}".format(self._sensors["location_sensor"].sense()))

    def _perceive(self):
        percept = {}
        for sensor in self._sensors:
            percept[sensor] = self._sensors[sensor].sense()
        return percept

    def _act(self, percept):
        action = self.function(percept)
    
        action_actuators = {
            "move": (self._actuators["mover"], ["direction"])
        }

        actuator, expected_params = action_actuators.get(action["name"], (None, None))                
        if actuator:
             args = [action["params"].get(param) for param in expected_params]
             actuator.act(*args)

    def behave(self):
        percept = self._perceive()
        self._act(percept)

