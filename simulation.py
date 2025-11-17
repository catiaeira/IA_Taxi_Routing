from Car_Controller import Car_Controller
from parser.parse_json_graph import parse_graph
from Client_Controller import Client_Controller
from Car_Controller import Car_Controller

def run(dynamic_traffic: bool, dynamic_car: bool, dynamic_client: bool): # the "main" loop
    graph = parse_graph()
    car_controller = Car_Controller(dynamic_car)
    client_controller = Client_Controller(dynamic_client)

    currTime = 0
    while (True):
        #option = main_menu()
        #if option == -1:
        #    break 

        # print (randomEvents(graph, car_controller, client_controller))

        # function to update the traffic (doesnt need a specific controller...) if dynamic
        # graph = update_traffic(graph)
        
        client_controller.update(currTime, graph)
        car_controller.update(currTime, client_controller, graph)
        currTime += 1


def main_menu():
    user_input = -1
    while user_input != 0:
        print("\n1 - Change cars")
        print("2 - Change clients")
        print("3 - Change traffic")
        print("4 - Skip to next time instance")
        print("5 - Skip to specific time instance")
        print("0 - Quit\n")

        user_input = int(input("Enter your option -> "))
        #user_input = 1

        match user_input:
            case 0:
                print("\nShutting down...")
                return -1

            case 1:
                # car
                return 0

            case 2:
                # clients
                return 0

            case 3:
                # traffic
                return 0

            case 4:
                # next time instance
                return 0

            case 5:
                # specific time instance
                return 0

            case _:
                print("Enter a valid option")

        _ = input("\nPress any key to continue")