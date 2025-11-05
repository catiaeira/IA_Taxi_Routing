class Car:
    def __init__(self, energy_level=100, capacity=4):
        self.kms_travelled: int = 0
        self.kms_travelled_w_passengers: int = 0
        self.energy_level = energy_level
        self.capacity: int = int (capacity)
        self.has_passenger = False

    # missing operational cost?

    def consumption (self, kms: int):
        return kms*self.consumption_per_km

    def assign_location (self, curr_node):
        self.curr_node: str = str(curr_node)
    

class ElectricCar(Car):
    def __init__(self, energy_level=100, capacity=4):
        super().__init__(energy_level, capacity)
        #self.consumption_per_km = 0.25 # 400km
        self.consumption_per_km = 0.5 # 200km <- for testing
 
    def CO2_emissions (self):
        return 0

    def charges_in (self):
        return "charging station"


class FuelCar (Car):
    def __init__(self, energy_level=100, capacity=4):
        super().__init__(energy_level, capacity)
        self.consumption_per_km = 0.1 # 1000 km

    def CO2_emissions (self):
        return 100 * kms_travelled

    def charges_in (self):
        return "fuel station"