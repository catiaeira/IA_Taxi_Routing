import math
from graph.Node import Node

def dist(latOr: float, longOr: float, latDest: float, longDest: float) -> float:
    lat1 = latOr * math.pi/180        #converted from decimal degrees to radians
    lat2 = latDest * math.pi/180

    long1 = longOr * math.pi/180
    long2 = longDest * math.pi/180

    #straigth line distance in kms - Haversine Formula
    distance = 2 * 6371 * math.asin(math.sqrt(math.pow(math.sin((lat2 - lat1)/2), 2) + math.cos(lat1)*math.cos(lat2)*math.pow(math.sin((long2 - long1)/2),2)))

    return distance


# returns the travel time in seconds
def calculate_time(dist: int, speed: int) -> float:
    return (dist/speed) * 3.6

