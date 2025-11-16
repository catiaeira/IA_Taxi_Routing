from graph.Energy_Station import Energy_Station
from parser.parse_json_graph import parse_graph
from car.Car import ElectricCar
from Client import Client


def do_trip (car, client): # basic trip logic, not dynamic
    if client.how_many > car.capacity - car.passengers_inside :
        print ("No capacity!") 
        return

    car_copy = car.copy()

    to_client = graph.procura_aStar(car_copy.curr_node, client.start, False)
    if to_client == None:
        print ("Can't get to client!") # no way there or not enough fuel
        return 
    
    car_copy.update_car_after_trip (to_client, False, client) # start ride 

    to_client_goal = graph.procura_aStar(car_copy.curr_node, client.goal, False)
    if to_client_goal == None:
        print ("Can't deliver client!") # no way there or not enough fuel
        return 

    car_copy.update_car_after_trip (to_client_goal, False, client)

    # if we get here the trip is possible, update status
    
    car.update_car_after_trip(to_client, True, client)
    car.update_car_after_trip(to_client_goal, True, client) # calling updatecar twice (for car and copy), find a better way?
    
    average_trip_cost = Car.total_kms_travelled_w_passengers / Car.total_trips_done
    kms_left = self.energy_level / car.consumption_per_km

    if average_trip_cost * 2 > kms_left:
        print ("Better charge")
        # set car goal to the closest energy station
        # to_station = graph.procura_aStar(car.curr_node, closestEnergyStationNode, True)
        # car.update_car_after_trip(to_station, True)
    else:
        print ("Good for now")


def main():
    graph = parse_graph()
    user_input = -1
    eCar = ElectricCar()

    while user_input != 0:
        print("\n1  - Print graph")
        print("2  - Draw graph")
        print("3  - Print nodes")
        print("4  - Print edges")
        print("5  - DFS")
        print("6  - BFS")
        print("7  - Dijkstra")
        print("8  - Greedy")
        print("9  - A*")
        print("10 - Find closest station (Dijkstra)")
        print("0  - Quit\n")

        user_input = int(input("Enter your option -> "))
        
        match user_input:
            case 0:
                print("\nBye")
                break

            case 1:
                print(graph.adjacency_lists_dict)

            case 2:
                graph.draw()

            case 3:
                print(graph.str_nodes())

            case 4:
                print(graph.str_edges())

            case 5:
                origin = input("Origin node -> ").lower().capitalize()
                destiny = input("Destiny node -> ").lower().capitalize()
                print(graph.procura_DFS(origin, destiny))

            case 6:
                origin = input("Origin node -> ").lower().capitalize()
                destiny = input("Destiny node -> ").lower().capitalize()
                print(graph.BFS_search(origin, destiny))

            case 7:
                origin = input("Origin node -> ").lower().capitalize()
                destiny = input("Destiny node -> ").lower().capitalize()
                print(graph.dijkstra_search(origin, destiny))

            case 8:
                origin = input("Origin node -> ").lower().capitalize()
                destiny = input("Destiny node -> ").lower().capitalize()
                print(graph.greedy(origin, destiny))

            case 9:
                origin = input("Origin node -> ").lower().capitalize()
                destiny = input("Destiny node -> ").lower().capitalize()
                

            case 10:
                origin = input("Origin node -> ").lower().capitalize()
                station = input("Station type -> ").upper()
                print(graph.find_closest_station(origin, Energy_Station.convert_from_str(station)))

            case _:
                print("Enter a valid option")

        _ = input("\nPress any key to continue")

if __name__ == "__main__":
    main()
