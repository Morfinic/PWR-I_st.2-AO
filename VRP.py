import numpy as np


class VRP:
    def __init__(self, locations: list[list], num_vehicles: int) -> None:
        self.locations = locations
        self.num_vehicles = num_vehicles
        self.num_clients = len(locations)

    def calculate_distance(self, location1: list, location2: list) -> float:
        return np.sqrt(np.pow(location1[0] - location2[0], 2) + np.pow(location1[1] - location2[1], 2))

