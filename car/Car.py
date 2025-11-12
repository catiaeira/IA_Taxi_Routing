from car.Energy_Station import Energy_Station

class Car:
    def __init__(self, energy_level : int =100, capacity: int =4):
        self.trips_done: int = 0
        self.kms_travelled: int = 0
        self.kms_travelled_w_passengers: int = 0
        self.energy_level : int = energy_level
        self.capacity: int = capacity
        self.has_passenger : bool = False
        self.curr_node : str = ""

    # missing operational cost?

    def consumption (self, kms: int) -> int:
        return kms*self.consumption_per_km

    def assign_location (self, curr_node :str):
        self.curr_node = curr_node


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