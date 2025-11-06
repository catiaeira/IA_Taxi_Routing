from parser.parse_json_graph import parse_graph
from Car import ElectricCar

def main():
    graph = parse_graph()
    user_input = -1
    eCar = ElectricCar(4)

    while user_input != 0:
        print("\n1 - Print graph")
        print("2 - Draw graph")
        print("3 - Print nodes")
        print("4 - Print edges")
        print("5 - DFS")
        print("6 - BFS")
        print("7 - A*")
        print("8 - Greedy")
        print("0 - Quit\n")

        user_input = int(input("Enter your option -> "))
        
        match user_input:
            case 0:
                print("\nBye")
                break

            case 1:
                print(graph.adjacency_lists_dict)

            case 2:
                graph.desenha()

            case 3:
                print(graph.adjacency_lists_dict.keys())

            case 4:
                print(graph.str_edges())

            case 5:
                origin = input("Origin node -> ")
                destiny = input("Destiny node -> ")
                print(graph.procura_DFS(origin, destiny))

            case 6:
                origin = input("Origin node -> ")
                destiny = input("Destiny node -> ")
                print(graph.BFS_search(origin, destiny))

            case 7:
                origin = input("Origin node -> ")
                destiny = input("Destiny node -> ")
                eCar.assign_location(origin)
                print(graph.procura_aStar(origin, destiny, eCar))

            case 8:
                origin = input("Origin node -> ")
                destiny = input("Destiny node -> ")
                print(graph.greedy(origin, destiny))

            case _:
                print("Enter a valid option")

        _ = input("\nPress any key to continue")

if __name__ == "__main__":
    main()
