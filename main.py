from graph.Energy_Station import Energy_Station
from parser.parse_json_graph import parse_graph
from car.Car import Car
from Client import Client
from tasks.Task_Deliver_Client import Task_Deliver_Client
from Car_Controller import Car_Controller
from Client_Controller import Client_Controller
from utils import is_int

def main():
    dynamic_traffic = True
    dynamic_car = True  
    dynamic_client = True
    roam = True

    graph = parse_graph()
    car_controller = Car_Controller(dynamic_car)
    client_controller = Client_Controller(dynamic_client, roam, graph)

    currTime = 0
    skipping = 0
    while (True):
        if skipping == 0: # if skipping forward, dont show the menu
            print ("Current time: " + str(currTime))
            option = main_menu(graph, car_controller, client_controller)
            if option == -1:
                break 
            elif option > 0:
                skipping = option 

        # print (randomEvents(graph, car_controller, client_controller))

        # function to update the traffic if dynamic
        graph_changed = graph.update_traffic(dynamic_traffic)
        # graph_changed = True # << for now
        
        client_controller.update(currTime, graph, roam)
        car_controller.update(currTime, client_controller, graph, graph_changed, roam)
        currTime += 1 
        if skipping > 0: 
            skipping -=1


def main_menu(graph, car_controller, client_controller):
    user_input = -1
    while user_input != 0:
        print("\n1 - Change cars")
        print("2 - Change clients")
        print("3 - Change traffic")
        print("4 - Skip to next time instance")
        print("5 - Specify the number of time instances skips")
        print("6 - Print the graph menu")
        print("7 - Change the algorithm used for pathing")
        print("8 - See global statistics")
        print("0 - Quit\n")

        user_input = input("Enter your option -> ")
        if not is_int(user_input):
            print("Invalid input, please enter a number.")
            continue

        match int(user_input):
            case 0:
                print("\nShutting down...")
                return -1

            case 1:
                car_menu (graph, car_controller)
                continue

            case 2:
                client_menu (graph, client_controller)
                continue

            case 3:
                traffic_menu(graph)
                continue

            case 4:
                # next time instance
                return 0

            case 5:
                # specific time instance
                skip_time = input ("Skip how many times? -> ")
                if not is_int(skip_time):
                    print("Invalid input, cancelling operation.")
                    continue
                if int(skip_time) <= 0:
                    print("Invalid value, cancelling operation.")
                    continue

                return int(skip_time)
                
            case 6:
                print_menu(graph)
                continue

            case 7:
                algorithm_menu(graph)
                continue

            case 8:
                global_stats_menu()
                continue

            case _:
                print("Invalid option, please try again.")

        _ = input("\nPress any key to continue")


def print_menu (graph):
    user_input = -1
    while user_input != 0:
        print("\n1 - Print graph")
        print("2 - Draw graph")
        print("3 - Draw directed graph")
        print("4 - Print nodes")
        print("5 - Print edges")
        print("0 - Go back\n")

        user_input = input("Enter your option -> ")
        if not is_int(user_input):
            print("Invalid input, please enter a number.")
            continue

        match int(user_input):
            case 0:
                return 0

            case 1:
                print(graph.adjacency_lists_dict)

            case 2:
                graph.draw()

            case 3:
                graph.draw_directed()

            case 4:
                print(graph.str_nodes())

            case 5:
                print(graph.str_edges())
            case _:
                print("Invalid option, please try again.")
                

def car_menu (graph, car_controller):
    user_input = -1
    while user_input != 0:
        print("\n1 - See cars")
        print("2 - Add car")
        print("3 - Delete car")
        print("4 - Change car")
        print("5 - Change car priority")
        print("6 - See simulation stats")
        print("0 - Go back\n")

        number_cars = car_controller.get_number_of_cars()

        user_input = input("Enter your option -> ")
        if not is_int(user_input):
            print("Invalid input, please enter a number.")
            continue

        match int(user_input):
            case 0:
                return
            
            case 1:
                car_controller.see_cars()

            case 2:
                print("1 - Fuel Car")
                print("2 - Electric Car\n")
                
                # car type
                car_type = input ("Enter your option -> ")
                if not is_int(car_type):
                    print("Invalid input, cancelling operation.")
                    continue
                
                if int(car_type) not in (1, 2):
                    print("Invalid option, cancelling operation.")
                    continue

                # car capacity
                car_capacity = input("Enter the car's capacity (Min. 3 / Max. 8) -> ")
                if not is_int(car_capacity):
                    print("Invalid input, cancelling operation.")
                    continue

                if not(3 <= int(car_capacity) <= 8):
                    print("Invalid amount, cancelling operation.")
                    continue

                # car energy level
                try:
                    car_energy_level = float(input("Enter the car's energy level -> "))
                except ValueError:
                    print("Invalid input, cancelling operation.")
                    continue

                if not(0 <= car_energy_level <= 100):
                    print("Invalid level, cancelling operation.")
                    continue

                #car current node
                car_curr_node = str(input("Enter the car's current location -> "))
                if not graph.node_exists(car_curr_node):
                    print("Node doesn't exist, cancelling operation.")
                    continue

                # car cost
                car_cost = input("Enter the car's cost (cent/km) (Min. 1 / Max. 10) -> ")
                if not is_int(car_cost):
                    print("Invalid input, cancelling operation.")
                    continue

                if not(1 <= int(car_capacity) <= 10):
                    print("Invalid amount, cancelling operation.")
                    continue

                car_controller.add_car(int(car_type), int(car_capacity), car_energy_level, car_curr_node, int(car_cost))
                car_controller.see_cars()
            
            case 3:
                car_controller.see_cars()
                print("Note that the numbering on the cars will change after a successful removal (unless the removed car is the last).")

                index = input("\nEnter the number of the car you wish to delete -> ")
                if not is_int(index):
                    print("Invalid input, cancelling operation.")
                    continue

                if not(0 <= int(index) < number_cars):
                    print("Invalid index, cancelling operation.")
                    continue

                car_controller.delete_car(int(index))
                car_controller.see_cars()
            
            case 4:
                car_controller.see_cars()

                # car index
                index = input("\nEnter the number of the car you wish to change -> ")
                if not is_int(index):
                    print("Invalid input, cancelling operation.")
                    continue

                if not(0 <= int(index) < number_cars):
                    print("Invalid index, cancelling operation.")
                    continue
            
                print("1 - Fuel Car")
                print("2 - Electric Car\n")
                
                # car type
                car_type = input ("Enter your option -> ")
                if not is_int(car_type):
                    print("Invalid input, cancelling operation.")
                    continue
                
                if int(car_type) not in (1, 2):
                    print("Invalid option, cancelling operation.")
                    continue

                # car capacity
                car_capacity = input("Enter the car's capacity (Min. 3 / Max. 8) -> ")
                if not is_int(car_capacity):
                    print("Invalid input, cancelling operation.")
                    continue

                if not(3 <= int(car_capacity) <= 8):
                    print("Invalid amount, cancelling operation.")
                    continue

                # car energy level
                try:
                    car_energy_level = float(input("Enter the car's energy level -> "))
                except ValueError:
                    print("Invalid input, cancelling operation.")
                    continue

                if not(0 <= car_energy_level <= 100):
                    print("Invalid level, cancelling operation.")
                    continue

                #car current node
                car_curr_node = str(input("Enter the car's current location -> "))
                if not graph.node_exists(car_curr_node):
                    print("Node doesn't exist, cancelling operation.")
                    continue
                
                car_controller.change_car(int(index), int(car_type), int(car_capacity), car_energy_level, car_curr_node)
                car_controller.see_cars()

            case 5:
                car_priority_menu(car_controller)   

            case 6:
                car_controller.see_sim_cars()
            case _:
                print("Invalid option, please try again.")

def car_priority_menu (car_controller):
    user_input = -1
    while user_input == -1:
        print ("\n1 - Time")
        print ("2 - Operational Cost")
        print ("0 - Go back\n")

        user_input = input("Enter your option -> ")
        if not is_int(user_input):
            print("Invalid input, please enter a number.")
            continue

        match int(user_input):
            case 0:
                return 0
            case 1:
                car_controller.CHOOSING_PREFERENCE = "TIME"
            case 2:
                car_controller.CHOOSING_PREFERENCE = "COST"
            case _:
                print("Invalid option, please try again.")
                user_input = -1
    return 0


def client_menu (graph, client_controller):
    user_input = -1
    while user_input != 0:
        print("\n1 - See clients")
        print("2 - Add client")
        print("3 - Delete client")
        print("4 - Change client")
        print("0 - Go back\n")

        number_waiting_clients = client_controller.get_n_waiting_clients()

        user_input = input("Enter your option -> ")
        if not is_int(user_input):
            print("Invalid input, please enter a number.")
            continue

        match int(user_input):
            case 0:
                return
            
            case 1:
                print("\nWaiting Clients:")
                client_controller.see_waiting_clients()
                print("\nClients On Route:")
                client_controller.see_clients_on_route()

            case 2:
                client_start = str(input("\nEnter the starting node -> "))
                if not graph.node_exists(client_start):
                    print("Node doesn't exist, cancelling operation.")
                    continue

                client_goal = str(input("Enter the destination node -> "))
                if not graph.node_exists(client_goal):
                    print("Node doesn't exist, cancelling operation.")
                    continue

                client_how_many = input("Enter the number of people taking the trip (Max. 8) -> ")
                if not is_int(client_how_many):
                    print("Invalid input, cancelling operation.")
                    continue

                if not (1 <= int(client_how_many) <= 8):
                    print("Invalid amount, cancelling operation.")
                    continue

                client_controller.add_client(client_start, client_goal, int(client_how_many))
                
                print("\nWaiting Clients:")
                client_controller.see_waiting_clients()
            
            case 3:
                print("\nWaiting Clients:")
                client_controller.see_waiting_clients()
                print("\nNote that the numbering on the clients will change after a successful removal (unless the removed client is the last).")

                index = input("\nEnter the number of the client you wish to delete -> ")
                if not is_int(index):
                    print("Invalid input, cancelling operation.")
                    continue
                
                if not(0 <= int(index) < number_waiting_clients):
                    print("Invalid index, cancelling operation.")
                    continue

                client_controller.delete_client(int(index))
                client_controller.see_waiting_clients()
            
            case 4:
                print("\nWaiting Clients:")
                client_controller.see_waiting_clients()
                
                index = input("\nEnter the number of the client you wish to change -> ")
                if not is_int(index):
                    print("Invalid input, cancelling operation.")
                    continue

                if not(0 <= int(index) < number_waiting_clients):
                    print("Invalid index, cancelling operation.")
                    continue
            
                client_start = str(input("\nEnter the starting node -> "))
                if not graph.node_exists(client_start):
                    print("Node doesn't exist, cancelling operation.")
                    continue

                client_goal = str(input("Enter the destination node -> "))
                if not graph.node_exists(client_goal):
                    print("Node doesn't exist, cancelling operation.")
                    continue

                client_how_many = input("Enter the number of people taking the trip (Max. 8) -> ")
                if not is_int(client_how_many):
                    print("Invalid input, cancelling operation.")
                    continue

                if not (1 <= int(client_how_many) <= 8):
                    print("Invalid amount, cancelling operation.")
                    continue
                
                client_controller.change_client(int(index), client_start, client_goal, int(client_how_many))
                print("\nWaiting Clients:")
                client_controller.see_waiting_clients()
            
            case _:
                print("Invalid option, please try again.")

def traffic_menu(graph):
    user_input = -1
    while user_input != 0:
        print("1 - Increase traffic")
        print("2 - Reduce traffic")
        print("3 - Randomize traffic")
        print("0 - Go back\n")

        user_input = input ("Enter your option -> ")
        if not is_int(user_input):
            print("Invalid input, please enter a number.")

        match int(user_input):
            case 0:
                return
            
            case 1:
                graph.change_traffic("up")
                continue

            case 2:
                graph.change_traffic("down")
                continue

            case 3:
                graph.change_traffic("random")
                continue

            case _:
                print("Invalid option, please try again.")
                continue


def algorithm_menu (graph):
    user_input = -1
    while user_input == -1:
        print("\n1 - DFS")
        print("2 - BFS")
        print("3 - Dijkstra")
        print("4 - Greedy")
        print("5 - A*")
        print("0 - Quit\n")

        user_input = input("Enter your option -> ")
        if not is_int(user_input):
            print("Invalid input, please enter a number.")
            continue

        match int(user_input):
            case 0:
                return 0
            case 1:
                graph.ALGORITHM = "DFS"
            case 2:
                graph.ALGORITHM = "BFS"
            case 3: 
                graph.ALGORITHM = "DIJKSTRA"
            case 4:
                graph.ALGORITHM = "GREEDY"
            case 5: 
                graph.ALGORITHM = "A_STAR"
            case _:
                print("Enter a valid option")
                user_input = -1
    return 0
    

def global_stats_menu ():
    if Car.total_trips_done > 0:
        avg_time = Task_Deliver_Client.total_time_trip / Car.total_trips_done
    else:
        avg_time = 0

    if Client_Controller.how_many_clients > 0:
        avg_waiting_time = Client_Controller.sum_waiting_time / Client_Controller.how_many_clients
    else:
        avg_waiting_time = 0

    print (f"Total trips done: {Car.total_trips_done}")
    print (f"Total kms travelled: {Car.total_kms_travelled}")
    print (f"Total kms travelled with clients: {Car.total_kms_travelled_w_passengers}")
    print (f"Operational costs (euros): {Car.total_operational_costs/100}")

    print (f"Average time taken per trip: {avg_time}")
    print (f"Average time client waits: {avg_waiting_time}")
    print (f"Most central node: {Client_Controller.central_popular_node}")

# operational cost 
    user_input = -1
    while user_input == -1:
        print("\n0 - Quit\n")

        user_input = input("Enter your option -> ")
        if not is_int(user_input):
            print("Invalid input, please enter a number.")
            continue

        match int(user_input):
            case 0:
                return 0
            case _:
                print("Enter a valid option")
                user_input = -1
    return 0

if __name__ == "__main__":
    main()
