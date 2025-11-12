from enum import Enum
 
class Energy_Station(Enum):
    NONE = 0
    CHARGING_STATION = 1
    FUEL_STATION = 2
    CHARGING_AND_FUEL_STATION = 3

    def convert_from_str (input : str):
        match (input):
            case ("FUEL_STATION"):
                return Energy_Station.FUEL_STATION
            case ("CHARGING_STATION"):
                return Energy_Station.CHARGING_STATION
            case ("CHARGING_AND_FUEL_STATION"):
                return Energy_Station.CHARGING_AND_FUEL_STATION
            case ("NONE"):
                return Energy_Station.NONE
            case (_):
                print ("error reading energy station type")
                return null
    