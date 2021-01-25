import json
from math import sqrt
from uuid import uuid4
from datetime import datetime
from .constants import DRIVER_DATA_CSV,  DEGREE_KMS, PINK
import pandas as pd


DRIVER_DF = pd.read_csv(DRIVER_DATA_CSV)
PINK_DRIVER_DF = None
RIDE_DATA = {}

class Distance_Service:

    def __init__(self, user_location=None):
        if user_location:
            DRIVER_DF['distance_from_user'] = DRIVER_DF.apply(self.calc_cars_distance_from_user, location2=user_location, axis=1)
            PINK_DRIVER_DF =  DRIVER_DF[DRIVER_DF['color'] == 'pink']


        # self.RIDE_DATA = {}
    def calc_cars_distance_from_user(self, row, location2):
        lat1 = row["latest_lat"]
        long1 = row["latest_long"]
        lat2 = location2["latitude"]
        long2 = location2["longitude"]
        diff_location = sqrt( ( (lat2 - lat1) ** 2 ) + ( (long2 - long1) ** 2 ) )
        distance = round(diff_location * DEGREE_KMS, 5)
        return distance



    def calc_two_location_distance(self, location1, location2):
        lat1 = location1["latitude"]
        long1 = location1["longitude"]
        lat2 = location2["latitude"]
        long2 = location2["longitude"]
        diff_location = sqrt( ( (lat2 - lat1) ** 2 ) + ( (long2 - long1) ** 2 ) )
        distance = round(diff_location * DEGREE_KMS, 5)
        return distance

class Driver_Service:
    def __init__(self, userId, location, cab_color):
        self.userId = userId
        self.cab_color = cab_color
        self.is_pink = cab_color.lower() == PINK
        self.user_latitude = location["latitude"]
        self.user_longitude = location["longitude"]
        self.distance_service = Distance_Service()
        self.push_notification = Push_Notification()


    def get_nearest_driver(self):
        NEAREST_DRIVER = None
        if self.is_pink:
            PINK_AVAIL_DRIVER_DF = PINK_DRIVER_DF[PINK_DRIVER_DF['available'] == True]
            MIN_DISTANCE = PINK_AVAIL_DRIVER_DF['distance_from_user'].min()
            NEAREST_DRIVER = PINK_AVAIL_DRIVER_DF.loc[PINK_AVAIL_DRIVER_DF['distance_from_user'] == MIN_DISTANCE, 'driverId']
        else:
            AVAIL_DRIVER_DF = DRIVER_DF[DRIVER_DF['available'] == True]
            MIN_DISTANCE = AVAIL_DRIVER_DF['distance_from_user'].min()
            NEAREST_DRIVER = str(AVAIL_DRIVER_DF.loc[AVAIL_DRIVER_DF['distance_from_user'] == MIN_DISTANCE, 'driverId'].values[0])
        return NEAREST_DRIVER


    def process_ride_request(self):
        nearest_driver = self.get_nearest_driver()
        if nearest_driver:
            rideId = uuid4()
            ride_obj = dict(user_id=self.userId, driver_id=nearest_driver, ride_id=rideId, cab_color=self.cab_color,
                            ride_state="Pending", ride_request_time=datetime.now())
            RIDE_DATA[rideId] = ride_obj
            self.push_notification.notify_driver(nearest_driver, rideId)
            return {"success": True, "ride_data": ride_obj}
        return {"success": False, "message": "NO DRIVERS AVAILABLE, Pls try after sometime" }



class Ride_Service:
    def __init__(self, rideId):
        self.rideId = rideId
        self.rideObj = RIDE_DATA.get(rideId)
        self.driverId = self.rideObj.get("driver_id")
        self.userId = self.rideObj.get("user_id")
        self.distance_service = Distance_Service()
        self.push_notification = Push_Notification()

    def ride_accepted(self):
        driverObj = DRIVER_DF[DRIVER_DF['driverId'] == self.driverId]
        DRIVER_DF.loc[DRIVER_DF['driverId'] == self.driverId, 'available'] = False
        RIDE_DATA[self.rideId]['ride_status'] = "Accepted"
        self.push_notification.notify_user(self.userId, driverObj)
        return True


    def ride_started(self, start_location):
        RIDE_DATA[self.rideId]['ride_status'] = "Started"
        RIDE_DATA[self.rideId]['start_lat'] = start_location['latitude']
        RIDE_DATA[self.rideId]['start_long'] = start_location['longitude']
        RIDE_DATA[self.rideId]['start_time'] = datetime.now()
        return True



    def ride_ended(self, destination_location):
        destination_time = datetime.now()
        RIDE_DATA[self.rideId]['ride_status'] = "Ended"
        RIDE_DATA[self.rideId]['destination_lat'] = destination_location['latitude']
        RIDE_DATA[self.rideId]['destination_long'] = destination_location['longitude']
        RIDE_DATA[self.rideId]['destination_time'] = destination_time

        DRIVER_DF.loc[DRIVER_DF['driverId'] == self.rideId, 'available'] = True

        start_lat = self.rideObj.get('start_lat')
        start_long = self.rideObj.get('start_long')
        start_location = {"latitude": start_lat, "longitude": start_long}
        distance_travelled = self.distance_service.calc_two_location_distance(start_location, destination_location)
        travel_time = destination_time - self.rideObj.get('start_time')
        travel_time_minutes = round(travel_time.seconds / 60 , 2)

        cab_color = self.rideObj.get("cab_color")
        price = round((1 * travel_time_minutes) + (2 * distance_travelled))
        if cab_color.lower() == PINK:
            price += 5

        RIDE_DATA[self.rideId]['price'] = price
        self.push_notification.notify_driver(self.driverId, price)
        self.push_notification.notify_user(self.userId, price)
        return {"success": True, "price": price, "distance_travelled": distance_travelled,
                "travel_time": travel_time}




class Push_Notification:

    def notify_driver(self, driverId, data):
        # fcm notify driver about ride
        pass

    def notify_user(self, userId, data):
        # fcm notify user about ride, driver  details
        pass
