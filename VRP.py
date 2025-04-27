import copy
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
            extra_client = 1 if free_client > 0 else 0
            free_client -= 1

            solutions[i] = clients[client_id:client_id + clients_for_vehicle + extra_client]
            client_id += clients_for_vehicle + extra_client

        return solutions

    def _calculate_total_route_distance(self, solutions) -> float:
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
            total_distance += self._calculate_distance(self.locations[route[-1]], self.locations[0])

        # Test kary za nierówne rozłożenie klientów
        # Nie wiem niby działa, ale czy to nie forcuje że nigdy nie przerzuci klienta na inny pojazd?
        # Można usunąć karę i wywalić przerzucanie na inną trasę i wyjdzie to samo
        clients_per_vehicle = self.num_clients / self.num_vehicles
        penalty = sum(abs(len(route) - clients_per_vehicle) for route in solutions) * 0
        return total_distance + penalty

    def _update_route(self, solutions):
        possible_moves = ["swap_client_order"]
        if self.num_vehicles > 1:
            possible_moves += ["swap_between_couriers", "change_courier"]
        move_type = random.choice(possible_moves)
        move = None

        new_sol = copy.deepcopy(solutions)

        if move_type == "swap_client_order":
            valid_couriers = [i for i, route in enumerate(new_sol) if len(route) >= 2]
            courier = random.choice(valid_couriers)

            c1, c2 = random.sample(range(len(new_sol[courier])), 2)

            new_sol[courier][c1], new_sol[courier][c2] = new_sol[courier][c2], new_sol[courier][c1]
            move = ("swap_client_order", courier, new_sol[courier][c1], new_sol[courier][c2])
        else:
            valid_couriers = [i for i, route in enumerate(new_sol) if len(route) > 0]
            if len(valid_couriers) < 2:
                return self._update_route(solutions)

            if move_type == "swap_between_couriers":
                courier1 = random.choice(valid_couriers)

                courier2 = random.choice([
                    x
                    for x in valid_couriers
                    if x != courier1
                ])

                c1 = random.randint(0, len(new_sol[courier1]) - 1)
                c2 = random.randint(0, len(new_sol[courier2]) - 1)

                new_sol[courier1][c1], new_sol[courier2][c2] = new_sol[courier2][c2], new_sol[courier1][c1]

                move = ("swap_between_couriers", courier1, courier2, new_sol[courier1][c1], new_sol[courier2][c2])
            elif move_type == "change_courier":
                courier1 = random.choice(valid_couriers)
                courier2 = random.choice([
                    x
                    for x in valid_couriers
                    if x != courier1
                ])

                client_id = random.randint(0, len(new_sol[courier1]) - 1)
                client = new_sol[courier1].pop(client_id)
                insert_pos = random.randint(0, len(new_sol[courier2]))
                new_sol[courier2].insert(insert_pos, client)

                move = ("change_courier", courier1, client, courier2, insert_pos)

        # Plaster na kod żeby nie zrzucał wszystko na jeden pojazd
        # Nie działa, poprostu zostawi minimum jeden na każdym pojeździe
        # if self.num_vehicles > 1:
        #     for route in new_sol:
        #         if len(route) == 0:
        #             return self._update_route(solutions)

        return new_sol, move

    def tabu_search(self, max_iter=100):
        current_solution = self._init_solution()
        current_cost = self._calculate_total_route_distance(current_solution)

        best_sol = copy.deepcopy(current_solution)
        best_cost = current_cost

        for _ in range(max_iter):
            best_change = None
            best_change_cost = float('inf')
            best_move = None

            for _ in range(10):
                new_sol, move = self._update_route(current_solution)
                new_cost = self._calculate_total_route_distance(new_sol)

                if not self._is_tabu(move) or new_cost < best_cost:
                    if new_cost < best_change_cost:
                        best_change = new_sol
                        best_change_cost = new_cost
                        best_move = move

            current_solution = best_change
            current_cost = best_change_cost
            self._update_tabu(best_move)

            if current_cost < best_cost:
                best_sol = copy.deepcopy(current_solution)
                best_cost = current_cost

        return [[0] + sol + [0] for sol in best_sol], best_cost
