import random
import numpy as np


class VRP:
    def __init__(self, locations: list[list], num_vehicles: int, tabu_limit: int = 3) -> None:
        self.locations = locations
        self.num_vehicles = num_vehicles
        self.num_clients = len(locations) - 1
        self.tabu_list = []
        self.tabu_limit = tabu_limit

    def _calculate_distance(self, location1: list, location2: list) -> float:
        return np.sqrt(np.pow(location1[0] - location2[0], 2) + np.pow(location1[1] - location2[1], 2))

    def _is_tabu(self, move):
        return move in self.tabu_list

    def _update_tabu(self, move):
        self.tabu_list.append(move)
        if len(self.tabu_list) > self.tabu_limit:
            self.tabu_list.pop(0)

    def _init_solution(self):
        clients = list(range(1, self.num_clients + 1))
        random.shuffle(clients)

        solutions = [[] for _ in range(self.num_vehicles)]
        clients_for_vehicle = len(clients) // self.num_vehicles
        free_client = len(clients) % self.num_vehicles

        client_id = 0
        for i in range(self.num_vehicles):
            extra_client = 1 if free_client < i else 0

            solutions[i] = clients[client_id:client_id + clients_for_vehicle + extra_client]
            client_id += clients_for_vehicle + extra_client

        return solutions

    def _calculate_route_distance(self, solutions) -> float:
        total_distance = 0

        for route in solutions:
            if not route:
                continue
            # Depot to first client
            total_distance += self._calculate_distance(self.locations[0], self.locations[route[0]])

            # Between clients
            for i in range(len(route) - 1):
                total_distance += self._calculate_distance(self.locations[route[i]], self.locations[route[i + 1]])

            # Last client to depot
            total_distance += self._calculate_distance(self.locations[route[-1]], self.locations[route[0]])

        return total_distance

    # TODO dodać losowość np. zamiana klientów między trasami, przerzucanie klientów na inną trasę
    def _update_route(self, solutions):
        pass

    def tabu_search(self):
        pass