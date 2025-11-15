import math
from graph.Node import Node

def dist(origin: Node, destination: Node) -> float:
    latOr = origin.getLatitude() * math.pi/180        #converted from decimal degrees to radians
    latDest = destination.getLatitude() * math.pi/180

    longOr = origin.getLongitude() * math.pi/180
    longDest = destination.getLongitude * math.pi/180

    #straigth line distance in kms - Haversine Formula
    distance = 2 * 6371 * math.asin(math.sqrt(math.pow(math.sin((latDest - latOr)/2), 2) + math.cos(latOr)*math.cos(latDest)*math.pow(math.sin((longDest - longOr)/2),2)))

    return distance