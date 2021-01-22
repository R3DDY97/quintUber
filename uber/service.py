import json
from math import sqrt
from datetime import datetime
from .models import  User, Driver, Pending_Ride, User_Ride
from .bst import Binary_Search_Tree

import pandas as pd

with open("./driver_dist.json", "r") as fp:
    driver_dist_dict = json.load(fp)

driver_df = pd.read_csv("./sample_driver_data.csv")


# source  https://docs.obspy.org/packages/autogen/obspy.geodetics.base.degrees2kilometers.html
DEGREE_KMS = 111.19492664455873

class Distance_Service:
    # def calc_two_location_distance(self, location1, location2):
    #     lat1 = location1.latitude
    #     long1 = location1.longitude
    #     lat2 = location2.latitude
    #     long2 = location2.longitude
    #     diff_location = sqrt( ( (lat2 - lat1) ** 2 ) + ( (long2 - long1) ** 2 ) )
    #     distance = round(diff_location * DEGREE_KMS, 2)
    #     return distance


    def calc_distance_from_origin(self, location):
        diff_location = sqrt((location.latitude ** 2) + (location.longitude ** 2))
        distance = round(diff_location * DEGREE_KMS, 2)
        return distance



class Driver_Service:
    def __init__(self, userId, location, cab_color):
        self.userId = userId
        self.cab_color = cab_color
        self.user_latitude = location.latitude
        self.user_longitude = location.longitude

    def get_available_drivers(self):
        available_drivers = Driver.objects.filter(available=True)
        return available_drivers


    def get_nearest_driver(self):
        available_drivers = self.get_available_drivers()
        if len(available_drivers) > 0:
            nearest_driver = 124
            return nearest_driver

    def process_ride_request(self):
        nearest_driver = self.get_nearest_driver()
        if nearest_driver:
            rideId = uuid4()
            User_Ride.objects.create(user_id=self.userId, driver_id=nearest_driver, ride_id=rideId, ride_state="Pending",
                                     ride_request_time=datetime.now())
            rideObj = User_Ride.get(ride_id=rideId)
            Push_Notification.notify_driver(nearest_driver, rideId)
            return {success: True, ride_data: rideObj}
        return {success: False, message: "NO DRIVERS AVAILABLE, Pls try after sometime" }



class Ride_Service:
    def __init__(self, rideId):
        self.rideId = rideId
        self.rideObj = User_Ride.objects.get(ride_id=rideId)
        self.driverId = self.rideObj.driver_id

    def ride_accepted(self):
        userId = self.rideObj.user_id
        driverObj = Driver.objects.get(driver_id=self.driverId)
        Driver.objects.filter(driver_id=self.driverId).update(available=False)
        User_Ride.objects.filter(ride_id=self.rideId).update(ride_status="Accepted")
        Push_Notification.notify_user(userId, driverObj)
        return True


    def ride_started(self, start_location):
        start_lat = start_location.latitude
        start_long = start_location.longitude
        start_time = datetime.now()
        ride_status = "Started"


    def ride_ended(self, dest_location):
        dest_lat = dest_location.latitude
        dest_long = dest_location.longitude
        driver_distance_from_origin = Distance_Service.distance_from_origin(dest_location)
        Driver.objects.filter(driver_id=self.driverId).update(available=True, latest_lat=dest_lat, latest_long=dest_long, distance_from_origin=driver_distance_from_origin)
        dest_time = datetime.now()
        travel_time = dest_time - self.rideObj.start_time
        travel_time_min = round(travel_time.seconds / 60 , 2)
        ride_status = "Ended"





class Push_Notification:

    def notify_driver(self, driverId, rideId):
        # fcm notify driver about ride
        pass

    def notify_user(self, userId, driverObj):
        # fcm notify user about ride, driver  details
        pass
