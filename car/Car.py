from typing_extensions import override
from car.Energy_Station import Energy_Station
from Client import Client
import copy

class Car:
    total_trips_done:int = 0
    total_kms_travelled:int = 0
    total_kms_travelled_w_passengers:int = 0
    total_trips_done:int = 0

    def __init__(self, energy_level : int =100, capacity: int =4):
        self.trips_done: int = 0
        self.kms_travelled: int = 0
        self.kms_travelled_w_passengers: int = 0
        self.energy_level: float = energy_level
        self.capacity: int = capacity
        self.passengers_inside : int = 0
        self.curr_node : str = ""

    # missing operational cost?

    def consumption (self, kms: int) -> int:
        return kms*self.consumption_per_km

    def assign_location (self, curr_node :str):
        self.curr_node = curr_node

    def update_car_after_trip (self, distance, new_fuel, count_for_global_stats : bool): 
        self.energy_level = new_fuel
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

            if client.goal == self.curr_node:
                self.trips_done += 1
                if count_for_global_stats:
                    Car.total_trips_done += 1
                self.passengers_inside -= client.how_many 
        
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
    def __init__(self, energy_level=100, capacity=4):
        super().__init__(energy_level, capacity)
        self.consumption_per_km = 0.25 # 400km
        #self.consumption_per_km = 0.5 # 200km <- for testing
 
    def CO2_emissions (self):
        return 0

    def charges_in (self) -> Energy_Station:
        return Energy_Station.CHARGING_STATION


class FuelCar (Car):
    def __init__(self, energy_level=100, capacity=4):
        super().__init__(energy_level, capacity)
        self.consumption_per_km = 0.1 # 1000 km

    def CO2_emissions (self):
        return 100 * kms_travelled

    def charges_in (self) -> Energy_Station:
        return Energy_Station.FUEL_STATION