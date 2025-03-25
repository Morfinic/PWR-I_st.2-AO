import numpy as np


class VRP:
    def __init__(self, locations, num_vehicles, tabu_limit=5):
        self.locations = [0, 0] + locations
        self.num_vehicles = num_vehicles
        self.num_clients = len(locations)
        self.tabu_list = []
        self.tabu_limit = tabu_limit

    def calculate_distance(self, location1, location2):
        return np.sqrt(np.pow(location1[0] - location2[0], 2) + np.pow(location1[1] - location2[1], 2))

    def tabu_search(self, iterations=100):
        pass