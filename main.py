import time
from car.Car import Car
from graph.Energy_Station import Energy_Station
from parser.parse_json_graph import parse_graph
from parser.get_osmnx_graph import get_graph


def main():
    osmnx = input("Load graph from OSMnx? [y/n]")

    if osmnx == "y":
        graph = get_graph()
        print("OSMnx graph successfully loaded")
    else:
        print("JSON graph successfully loaded")
        graph = parse_graph()

    user_input = -1

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
        print("12 - Find closest available car (Dijkstra)")
        print("13 - Find route with the most nodes (A*)")
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

                start = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
                print(graph.DFS_search(origin, destination))
                end = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
                print(f"Time elapsed: {(end-start)/1_000_000}ms")

            case 7:
                origin = input("Origin node -> ").lower().capitalize()
                destination = input("Destination node -> ").lower().capitalize()

                start = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
                print(graph.BFS_search(origin, destination))
                end = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
                print(f"Time elapsed: {(end-start)/1_000_000}ms")

            case 8:
                origin = input("Origin node -> ").lower().capitalize()
                destination = input("Destination node -> ").lower().capitalize()

                start = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
                print(graph.dijkstra_search(origin, destination))
                end = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
                print(f"Time elapsed: {(end-start)/1_000_000}ms")

            case 9:
                origin = input("Origin node -> ").lower().capitalize()
                destination = input("Destination node -> ").lower().capitalize()

                start = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
                print(graph.greedy_search(origin, destination))
                end = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
                print(f"Time elapsed: {(end-start)/1_000_000}ms")

            case 10:
                origin = input("Origin node -> ").lower().capitalize()
                destination = input("Destination node -> ").lower().capitalize()

                start = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
                print(graph.a_star_search(origin, destination))
                end = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
                print(f"Time elapsed: {(end-start)/1_000_000}ms")

            case 11:
                origin = input("Origin node -> ").lower().capitalize()
                station = input("Station type -> ").upper()

                start = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
                print(graph.find_closest_station(origin, Energy_Station.convert_from_str(station)))
                end = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
                print(f"Time elapsed: {(end-start)/1_000_000}ms")

            case 12:
                origin = input("Origin node -> ").lower().capitalize()
                cars: set[Car] = set()
                print("Enter nodes with available cars (type 'end' when you're done)")
                while True:
                    node = input("Available car -> ").lower().capitalize()
                    if node == "End":
                        break
                    car = Car()
                    car.assign_location(node)
                    cars.add(car)

                start = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
                print(graph.find_closest_car(origin, cars))
                end = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
                print(f"Time elapsed: {(end-start)/1_000_000}ms")

            case 13:
                origin = input("Origin node -> ").lower().capitalize()
                start = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
                print(graph.find_longest_route(origin))
                end = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
                print(f"Time elapsed: {(end-start)/1_000_000}ms")

            case _:
                print("Enter a valid option")

        _ = input("\nPress any key to continue")

if __name__ == "__main__":
    main()
