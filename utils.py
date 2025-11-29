import math
from graph.Node import Node

def dist(latOr: float, longOr: float, latDest: float, longDest: float) -> float:
    lat1 = latOr * math.pi/180        #converted from decimal degrees to radians
    lat2 = latDest * math.pi/180

    long1 = longOr * math.pi/180
    long2 = longDest * math.pi/180

    #straigth line distance in kms - Haversine Formula
    distance = 2 * 6371 * math.asin(math.sqrt(math.pow(math.sin((lat2 - lat1)/2), 2) + math.cos(lat1)*math.cos(lat2)*math.pow(math.sin((long2 - long1)/2),2)))

    return distance


# returns the travel time in seconds
def calculate_time(dist: int, speed: int) -> float:
    return (dist/speed) * 3.6

# returns in minutes
def calc_time_between_nodes(curr_node: str, goal_node : str, graph) -> float:
        distance = graph.get_arc_distance(curr_node, goal_node) # in meters
        speed = graph.get_arc_speed(curr_node, goal_node)       # in km/h
        if (distance == math.inf or speed == math.inf):
            print (f"Path not found when calculating time: {curr_node} - {goal_node}")
            return 0

        time = distance / 1000 / speed * 60
        return time

# uses the car's current node as the starting point to create the path 
def create_path_to_client(graph, car, client) -> tuple[list[str], float, int] | None:
    return create_path_to_client_and_goal(graph, car, client, car.curr_node)

# creates the entire path from the given origin node to the client and then to the goal
def create_path_to_client_and_goal(graph, car, client, origin_node: str) -> tuple[list[str], float, int] | None:
    if client.how_many > car.capacity - car.passengers_inside:
        print("No capacity!") 
        return None

    # Car to Client 
    to_client = graph.a_star_search(origin_node, client.start)
    if to_client is None:
        print(f"Can't get from {origin_node} to client {client.start}!")
        return None
    to_client_path, to_client_time, to_client_dist = to_client

    if not is_trip_feasible(car, to_client_dist, car.energy_level):
        print("Runs out of fuel going to client!")
        return None

    # Client to Goal
    to_goal = graph.a_star_search(client.start, client.goal)
    if to_goal is None:
        print(f"Can't deliver client from {client.start} to goal {client.goal}!")
        return None
    to_goal_path, to_goal_time, to_goal_dist = to_goal
    

    total_dist_meters = to_client_dist + to_goal_dist
    if not is_trip_feasible(car, total_dist_meters, car.energy_level):
        print("Runs out of fuel delivering client!")
        return None

    total_time = to_client_time + to_goal_time
    
    if to_goal_path and to_goal_path[0] == client.start and len(to_goal_path[0])>2: 
        to_goal_path.pop(0) # remove head of list, since itll be redundant 
        
    total_path = to_client_path + to_goal_path

    return total_path, total_time, total_dist_meters


def update_path(graph, car, client, last_completed_node: str) -> tuple[list[str], float, int] | None:    
    if not client.is_in_car:
        return create_path_to_client_and_goal(graph, car, client, last_completed_node)
    else:
        return path_to_goal_only(graph, car, client, last_completed_node)


def path_to_goal_only(graph, car, client, origin_node: str) -> tuple[list[str], float, int] | None:
    to_goal = graph.a_star_search(origin_node, client.goal)
    if to_goal is None:
        print(f"Can't find a path from {origin_node} to goal {client.goal}!")
        return None
    
    path, time, dist = to_goal
    
    if not is_trip_feasible(car, dist, car.energy_level):
        print("Runs out of fuel on the way to the goal!")
        return None
        
    if path and path[0] == origin_node and len(path)>2: 
        path.pop(0)                     # remove head of list, since itll be redundant 

    return path, time, dist


def is_trip_feasible(car, total_distance_meters, initial_energy_level) -> bool:
    distance_km = total_distance_meters / 1000
    energy_needed = car.consumption(distance_km)
    
    final_energy = initial_energy_level - energy_needed
    
    return final_energy >= 0