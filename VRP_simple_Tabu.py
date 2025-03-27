from VRP import VRP


class VRP_Tabu(VRP):
    def __init__(self,
                 locations: list[list], num_vehicles: int,
                 tabu_limit: int
                 ) -> None:
        super().__init__(locations, num_vehicles)
        self.tabu_list = []
        self.tabu_limit = tabu_limit
