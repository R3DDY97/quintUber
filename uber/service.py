import json
from math import sqrt
from datetime import datetime
# from .models import  User, Driver, Pending_Ride, User_Ride
from .binary_search_tree import Tree
from .constants import DRIVER_DATA_CSV, DRIVER_DIST_JSON, PINK_DRIVER_DIST_JSON, DEGREE_KMS, PINK
import pandas as pd



class Memory_Data:
    def __init__(self):
        self.DRIVER_DIST_MAP = self.get_driver_dist(DRIVER_DIST_JSON)
        self.PINK_DRIVER_DIST_MAP = self.get_driver_dist(PINK_DRIVER_DIST_JSON)

        self.DRIVER_DIST_LIST = list(self.DRIVER_DIST_MAP.keys())
        self.PINK_DRIVER_DIST_LIST = list(self.PINK_DRIVER_DIST_MAP.keys())

        self.DRIVER_DF = pd.read_csv(DRIVER_DATA_CSV)

        self.DISTANCE_TREE = self.get_bst(self.DRIVER_DIST_LIST)
        self.PINK_DISTANCE_TREE = self.get_bst(self.PINK_DRIVER_DIST_LIST)

        self.RIDE_DATA = {}


    def get_driver_dist(self, filename):
        with open(filename, "r") as fp:
            driver_dist_dict = json.load(fp)
            return driver_dist_dict


    def get_bst(self, distance_list):
        # build bst using drivers distances from origin
        DISTANCE_TREE = Tree()
        for dist in distance_list:
            DISTANCE_TREE.add_node(float(dist))
        return DISTANCE_TREE

    def get_drivers_list(self):
        avail_drivers_df = self.DRIVER_DF[self.DRIVER_DF['available'] == True]
        return avail_drivers_df.to_dict(orient="records")


memory_data = Memory_Data()



class Distance_Service:
    def calc_two_location_distance(self, location1, location2):
        lat1 = location1.latitude
        long1 = location1.longitude
        lat2 = location2.latitude
        long2 = location2.longitude
        diff_location = sqrt( ( (lat2 - lat1) ** 2 ) + ( (long2 - long1) ** 2 ) )
        distance = round(diff_location * DEGREE_KMS, 2)
        return distance


    def calc_distance_from_origin(self, location):
        diff_location = sqrt((location.latitude ** 2) + (location.longitude ** 2))
        distance = round(diff_location * DEGREE_KMS, 5)
        return distance



class Driver_Service:
    def __init__(self, userId, location, cab_color):
        self.userId = userId
        self.cab_color = cab_color
        self.is_pink = cab_color.lower() == PINK
        self.user_latitude = location.latitude
        self.user_longitude = location.longitude
        self.user_dist_from_origin = Distance_Service.distance_from_origin(location)


    # def get_available_drivers(self):
    #     if self.is_pink:
    #         available_drivers = Driver.objects.filter(available=True, cab_color=PINK)
    #     else:
    #         available_drivers = Driver.objects.filter(available=True)
    #     return available_drivers

    def get_memory_available_drivers(self):
        available_drivers = None
        if self.is_pink:
            available_drivers = list(memory_data.PINK_DRIVER_DIST_MAP.values())
        else:
            available_drivers = list(memory_data.DRIVER_DIST_MAP.values())
        return available_drivers


    def get_nearest_driver(self):
        # available_drivers = self.get_available_drivers()
        available_drivers = self.get_memory_available_drivers()
        nearest_driver = None
        if len(available_drivers) > 0:
            if self.is_pink:
                nearest_node = memory_data.PINK_DISTANCE_TREE.search(self.user_dist_from_origin)
                nearest_driver = memory_data.PINK_DRIVER_DIST_MAP.pop(node.key)
                memory_data.PINK_DISTANCE_TREE.delete_node(nearest_node)
            else:
                nearest_node = memory_data.DISTANCE_TREE.search(self.user_dist_from_origin)
                nearest_driver = memory_data.DRIVER_DIST_MAP.pop(node.key)
                memory_data.DISTANCE_TREE.delete_node(nearest_node)
            return nearest_driver




    def process_ride_request(self):
        nearest_driver = self.get_nearest_driver()
        if nearest_driver:
            rideId = uuid4()
            ride_obj = dict(user_id=self.userId, driver_id=nearest_driver, ride_id=rideId, cab_color=cab_color,
                            ride_state="Pending", ride_request_time=datetime.now())
            memory_data.RIDE_DATA[rideId] = ride_obj
            Push_Notification.notify_driver(nearest_driver, rideId)
            return {success: True, ride_data: ride_obj}
        return {success: False, message: "NO DRIVERS AVAILABLE, Pls try after sometime" }




# class Ride_Service:
#     def __init__(self, rideId):
#         self.rideId = rideId
#         self.rideObj = User_Ride.objects.get(ride_id=rideId)
#         self.driverId = self.rideObj.driver_id

#     def ride_accepted(self):
#         userId = self.rideObj.user_id
#         driverObj = Driver.objects.get(driver_id=self.driverId)
#         Driver.objects.filter(driver_id=self.driverId).update(available=False)
#         User_Ride.objects.filter(ride_id=self.rideId).update(ride_status="Accepted")
#         Push_Notification.notify_user(userId, driverObj)
#         return True


#     def ride_started(self, start_location):
#         start_lat = start_location.latitude
#         start_long = start_location.longitude
#         start_time = datetime.now()
#         ride_status = "Started"


#     def ride_ended(self, dest_location):
#         dest_lat = dest_location.latitude
#         dest_long = dest_location.longitude
#         driver_distance_from_origin = Distance_Service.distance_from_origin(dest_location)
#         Driver.objects.filter(driver_id=self.driverId).update(available=True, latest_lat=dest_lat, latest_long=dest_long, distance_from_origin=driver_distance_from_origin)
#         dest_time = datetime.now()
#         travel_time = dest_time - self.rideObj.start_time
#         travel_time_min = round(travel_time.seconds / 60 , 2)
#         ride_status = "Ended"

# use memory data - dict , df
class Ride_Service:
    def __init__(self, rideId):
        self.rideId = rideId
        self.rideObj = memory_data.RIDE_DATA.get(rideId)
        self.driverId = self.rideObj.get("driver_id")

    def ride_accepted(self):
        userId = self.rideObj.user_id
        driverObj = memory_data.DRIVER_DF[memory_data.DRIVER_DF['driver_id'] == self.driverId]
        memory_data.DRIVER_DF.loc[memory_data.DRIVER_DF['driverId'] == self.driverId, 'available'] = False
        memory_data.RIDE_DATA[rideId]['ride_status'] = "Accepted"
        # Driver.objects.filter(driver_id=self.driverId).update(available=False)
        # User_Ride.objects.filter(ride_id=self.rideId).update(ride_status="Accepted")
        Push_Notification.notify_user(userId, driverObj)
        return True


    def ride_started(self, start_location):
        memory_data.RIDE_DATA[rideId]['ride_status'] = "Started"
        memory_data.RIDE_DATA[rideId]['start_lat'] = start_location.latitude
        memory_data.RIDE_DATA[rideId]['start_long'] = start_location.longitude
        memory_data.RIDE_DATA[rideId]['start_time'] = datetime.now()



    def ride_ended(self, dest_location):
        destination_time = datetime.now()
        memory_data.RIDE_DATA[rideId]['ride_status'] = "Ended"
        memory_data.RIDE_DATA[rideId]['destination_lat'] = destination_location.latitude
        memory_data.RIDE_DATA[rideId]['destination_long'] = destination_location.longitude
        memory_data.RIDE_DATA[rideId]['destination_time'] = destination_time

        memory_data.DRIVER_DF.loc[memory_data.DRIVER_DF['driverId'] == rideId, 'available'] = True

        start_lat = self.rideObj.get('start_lat')
        start_long = self.rideOb.get('start_long')
        start_location = {"start_latitude": start_lat, "start_longitude": start_long}
        distance_travelled = Distance_Service.calc_two_location_distance(start_location, dest_location)
        travel_time = destination_time - self.rideObj.get('start_time')
        travel_time_minutes = round(travel_time.seconds / 60 , 2)
        driver_dist_from_origin = Distance_Service.calc_distance_from_origin(dest_location)

        cab_color = self.rideObj.get("cab_color")
        price = round((1 * travel_time_minutes) + (2 * distance_travelled))
        if cab_color.lower() == PINK:
            price += 5
            memory_data.PINK_DRIVER_DIST_MAP[driver_dist_from_origin] = self.driveId
            memory_data.PINK_DISTANCE_TREE.add_node(driver_dist_from_origin)
        else:
            memory_data.DRIVER_DIST_MAP[driver_dist_from_origin] = self.driveId
            memory_data.DISTANCE_TREE.add_node(driver_dist_from_origin)

        memory_data.RIDE_DATA[rideId]['price'] = price
        Push_Notification.notify_driver(driveId, price)
        Push_Notification.notify_user(userId, price)





class Push_Notification:

    def notify_driver(self, driverId, data):
        # fcm notify driver about ride
        pass

    def notify_user(self, userId, data):
        # fcm notify user about ride, driver  details
        pass
