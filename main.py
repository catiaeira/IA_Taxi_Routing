from graph.Energy_Station import Energy_Station
from parser.parse_json_graph import parse_graph
from car.Car import ElectricCar
from Client import Client
from Car_Controller import Car_Controller
from Client_Controller import Client_Controller

def main():
    dynamic_traffic = False
    dynamic_car = False  
    dynamic_client = False  

    graph = parse_graph()
    car_controller = Car_Controller(dynamic_car)
    client_controller = Client_Controller(dynamic_client)

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
        # graph, graph_changed = update_traffic(graph)
        graph_changed = True # << for now
        
        client_controller.update(currTime, graph)
        car_controller.update(currTime, client_controller, graph, graph_changed)
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
        print("0 - Quit\n")

        user_input = int(input("Enter your option -> "))
        #user_input = 1

        match user_input:
            case 0:
                print("\nShutting down...")
                return -1

            case 1:
                car_menu (car_controller)
                continue

            case 2:
                client_menu (client_controller)
                continue

            case 3:
                print ("traffic")
                continue

            case 4:
                # next time instance
                return 0

            case 5:
                # specific time instance
                skip_time = int (input ("Skip how many times? -> "))
                # needs validation ^^^
                return skip_time
                
            case 6:
                print_menu(graph)
                continue

            case 7:
                algorithm_menu(graph)
                continue

            case _:
                print("Enter a valid option")

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

        user_input = int(input("Enter your option -> "))

        match user_input:
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
                print("Enter a valid option")
                

def car_menu (car_controller):  # not yet implemented
    user_input = -1
    while user_input != 0:
        print("\n1 - See cars")
        print("2 - Add car")
        print("3 - Delete car")
        print("4 - Change car")
        print("0 - Go back\n")

        user_input = int(input("Enter your option -> "))

        match user_input:
            case 0:
                return 0


def client_menu (client_controller):    # not yet implemented
    user_input = -1
    while user_input != 0:
        print("\n1 - See clients")
        print("2 - Add client")
        print("3 - Delete client")
        print("4 - Change client")
        print("0 - Go back\n")

        user_input = int(input("Enter your option -> "))

        match user_input:
            case 0:
                return 0


def algorithm_menu (graph):
    user_input = -1
    while user_input == -1:
        print("\n1 - DFS")
        print("2 - BFS")
        print("3 - Dijkstra")
        print("4 - Greedy")
        print("5 - A*")
        print("0 - Quit\n")

        user_input = int(input("Enter your option -> "))

        match user_input:
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
    


if __name__ == "__main__":
    main()
