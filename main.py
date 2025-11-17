from parser.parse_json_graph import parse_graph
from car.Car import ElectricCar
from Client import Client
from simulation import run

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
    run(False, False, False)

if __name__ == "__main__":
    main()
