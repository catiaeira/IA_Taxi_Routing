import math
from car.Car import Car

def dist(latOr: float, longOr: float, latDest: float, longDest: float) -> float:
    lat1 = latOr * math.pi/180        #converted from decimal degrees to radians
    lat2 = latDest * math.pi/180

    long1 = longOr * math.pi/180
    long2 = longDest * math.pi/180

    #straigth line distance in kms - Haversine Formula
    distance = 2 * 6371 * math.asin(math.sqrt(math.pow(math.sin((lat2 - lat1)/2), 2) + math.cos(lat1)*math.cos(lat2)*math.pow(math.sin((long2 - long1)/2),2)))

    return distance * 1000


# returns the travel time in seconds
def calculate_time(dist: int, speed: int) -> float:
    if speed == 0:
        return 0
    return (dist/speed) * 3.6

def is_trip_feasible(car: Car, total_distance_meters: int) -> bool:
    distance_km = total_distance_meters / 1000
    energy_needed = car.consumption(distance_km)
    
    final_energy = car.energy_level - energy_needed
    
    return final_energy >= 0


def is_int(input: str) -> bool:
    try:
        i = int(input)
        return True
    except ValueError:
        return False
