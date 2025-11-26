from Car_Controller import Car_Controller
from parser.parse_json_graph import parse_graph
from Client_Controller import Client_Controller
from Car_Controller import Car_Controller


while user_input != 0:
    print("\n1  - Print graph")
    print("2  - Draw graph")
    print("3  - Draw directed graph")
    print("4  - Print nodes")
    print("5  - Print edges")
    print("6  - DFS")
    print("7  - BFS")
    print("8  - Dijkstra")
    print("9  - Greedy")
    print("10 - A*")
    print("11 - Find closest station (Dijkstra)")
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
            graph.draw_directed()

        case 4:
            print(graph.str_nodes())

        case 5:
            print(graph.str_edges())

        case 6:
            origin = input("Origin node -> ").lower().capitalize()
            destination = input("Destination node -> ").lower().capitalize()
            print(graph.procura_DFS(origin, destination))

        case 7:
            origin = input("Origin node -> ").lower().capitalize()
            destination = input("Destination node -> ").lower().capitalize()
            print(graph.BFS_search(origin, destination))

        case 8:
            origin = input("Origin node -> ").lower().capitalize()
            destination = input("Destination node -> ").lower().capitalize()
            print(graph.dijkstra_search(origin, destination))

        case 9:
            origin = input("Origin node -> ").lower().capitalize()
            destination = input("Destination node -> ").lower().capitalize()
            print(graph.greedy(origin, destination))

        case 10:
            origin = input("Origin node -> ").lower().capitalize()
            destination = input("Destination node -> ").lower().capitalize()
            print(graph.a_star_search(origin, destination))

        case 11:
            origin = input("Origin node -> ").lower().capitalize()
            station = input("Station type -> ").upper()
            print(graph.find_closest_station(origin, Energy_Station.convert_from_str(station)))

        case _:
            print("Enter a valid option")

    _ = input("\nPress any key to continue")