from typing_extensions import override
from graph.Energy_Station import Energy_Station
from Client import Client
import copy

class Car:
    total_trips_done:int = 0
    total_kms_travelled:int = 0
    total_kms_travelled_w_passengers:int = 0

    # op cost is in cents per km
    def __init__(self, trips_done: int =0, kms_travelled: int =0, kms_travelled_w_passengers: int =0, energy_level: float =100, capacity: int =4, passengers_inside: int =0, curr_node: str ="", op_cost_km: int = 40):
        self.trips_done: int = trips_done
        self.kms_travelled: int = kms_travelled
        self.kms_travelled_w_passengers: int = kms_travelled_w_passengers
        self.energy_level: float = energy_level
        self.capacity: int = capacity
        self.passengers_inside : int = passengers_inside
        self.curr_node : str = curr_node
        self.op_cost_km: int = op_cost_km


    def change_characteristics(self, car_type: int, car_capacity: int, car_energy_level: int, car_curr_node: str):
        if car_type == 1:
            new_car = FuelCar(self.trips_done, self.kms_travelled, self.kms_travelled_w_passengers, car_energy_level, car_capacity, self.passengers_inside, car_curr_node)
        elif car_type == 2:
            new_car = ElectricCar(self.trips_done, self.kms_travelled, self.kms_travelled_w_passengers, car_energy_level, car_capacity, self.passengers_inside, car_curr_node)
        return new_car

    def consumption (self, kms: float) -> float:
        return kms*self.consumption_per_km

    def assign_location (self, curr_node :str):
        self.curr_node = curr_node

    def update_car_after_trip (self, distance_meters :int, count_for_global_stats : bool): 
        distance = distance_meters / 1000
        self.energy_level -= self.consumption(distance)
        if count_for_global_stats:
            Car.total_kms_travelled += distance
        self.kms_travelled += distance

        if self.passengers_inside > 0:
            if count_for_global_stats:
                Car.total_kms_travelled_w_passengers += distance
            self.kms_travelled_w_passengers += distance


    def update_car_clients (self, count_for_global_stats : bool, client : Client): 
        if client is not None:
            if client.start == self.curr_node:
                self.passengers_inside += client.how_many 
                print ("added clients to car")

            if client.goal == self.curr_node:
                self.trips_done += 1
                if count_for_global_stats:
                    Car.total_trips_done += 1
                self.passengers_inside -= client.how_many 
                print ("removed clients from car")
        
    def copy(self):
        return copy.copy(self)

    @override
    def __str__(self) -> str:
        return (
            f"Car ("
            f"trips_done = {self.trips_done}, "
            f"kms_travelled = {self.kms_travelled}, "
            f"kms_travelled_w_passengers = {self.kms_travelled_w_passengers}, "
            f"energy_level = {self.energy_level}%, "
            f"capacity = {self.capacity}, "
            f"number of passengers = {self.passengers_inside}, "
            f"curr_node = '{self.curr_node}')"
        )


class ElectricCar (Car):
    def __init__(self, trips_done: int =0, kms_travelled: int =0, kms_travelled_w_passengers: int =0, energy_level: float =100, capacity: int =4, passengers_inside: int =0, curr_node: str ="", op_cost_km: int = 40):
        super().__init__(trips_done, kms_travelled, kms_travelled_w_passengers, energy_level, capacity, passengers_inside, curr_node, op_cost_km)
        self.consumption_per_km = 0.25 # 400km
        #self.consumption_per_km = 0.5 # 200km <- for testing
 
    def CO2_emissions (self):
        return 0

    def charges_in (self) -> Energy_Station:
        return Energy_Station.CHARGING_STATION

    def time_to_refuel(self) -> int: 
        return (100 - self.energy_level) / 4     # could change between cars. 25 mins to fully recharge

    @override
    def __str__(self) -> str:
        return "Electric " + super().__str__()


class FuelCar (Car):
    def __init__(self, trips_done: int =0, kms_travelled: int =0, kms_travelled_w_passengers: int =0, energy_level: float =100, capacity: int =4, passengers_inside: int =0, curr_node: str ="", op_cost_km: int = 40):
        super().__init__(trips_done, kms_travelled, kms_travelled_w_passengers, energy_level, capacity, passengers_inside, curr_node, op_cost_km)
        self.consumption_per_km = 0.1 # 1000 km

    def CO2_emissions (self):
        return 100 * self.kms_travelled

    def charges_in (self) -> Energy_Station:
        return Energy_Station.FUEL_STATION

    def time_to_refuel (self) -> int:
        return 5 # minutes

    @override
    def __str__(self) -> str:
        return "Fuel " + super().__str__()
