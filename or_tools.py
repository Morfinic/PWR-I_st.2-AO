import numpy as np
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

def _calculate_distance(location1: list, location2: list) -> float:
    return np.sqrt(np.pow(location1[0] - location2[0], 2) + np.pow(location1[1] - location2[1], 2))

def create_datamodel(dataset):
    data = {
        'distance_matrix': [],
        'num_vehicles' : dataset["num_of_vehicles"],
        'depot' : 0,
    }
    locations = dataset['data']


    for i in range(len(locations)):
        tmpTab = []
        for j in range(len(locations)):
            distance = _calculate_distance(locations[i], locations[j]) if i != j else 0
            tmpTab.append(int(distance * 1000))
        data['distance_matrix'].append(tmpTab)

    return data

def get_routes_and_distance(manager, routing, solution, data):
    routes = []
    total_distance = 0

    for vehicle_id in range(manager.GetNumberOfVehicles()):
        route = []
        route_distance = 0
        idx = routing.Start(vehicle_id)

        while not routing.IsEnd(idx):
            node = manager.IndexToNode(idx)
            route.append(node)
            prev_idx = idx
            idx = solution.Value(routing.NextVar(idx))
            route_distance += routing.GetArcCostForVehicle(prev_idx, idx, vehicle_id)

        node = manager.IndexToNode(idx)
        route.append(node)

        routes.append(route)
        total_distance += route_distance

    total_distance /= 1000

    return routes, total_distance

def or_tools_solve(dataset):
    data = create_datamodel(dataset)
    manager = pywrapcp.RoutingIndexManager(
        len(data['distance_matrix']),
        data['num_vehicles'],
        data['depot']
    )
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,
        3000 * 1000,
        True,
        dimension_name
    )
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        # Init sol
        routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION
    )
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.TABU_SEARCH
    )
    search_parameters.time_limit.seconds = 30
    # search_parameters.log_search = True

    solution = routing.SolveWithParameters(search_parameters)

    return get_routes_and_distance(manager, routing, solution, data)