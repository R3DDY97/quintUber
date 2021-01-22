from .models import  User, Driver, Pending_Ride, User_Ride

class Driver_Service:
    def __init__(self, userId, location, cab_color):
        self.userId = userId
        self.cab_color = cab_color
        self.latitude = location.latitude
        self.longitude = location.longitude

    def get_available_drivers(self):
        available_drivers = 100
        return available_drivers


    def get_nearest_driver(self):
        available_drivers = self.get_available_drivers()
        if len(available_drivers) > 0:
            nearest_driver = 124
            return nearest_driver


class Ride_Service:
    def __init__(self, rideId):
        self.rideId = rideId
        self.rideObj = User_Ride.objects.get(ride_id=rideId)

    def ride_accepted(self):
        driverId = self.rideObj.driver_id
        userId = self.rideObj.user_id
        driverObj = Driver.objects.get(driver_id=driverId)
        User_Ride.objects.filter(driver_id=driverId).update(available=False)
        Push_Notification.notify_user(userId, driverObj)
        return True


    def ride_started(self):
        pass

    def ride_ended(self):
        pass




class Push_Notification:

    def notify_driver(self, driverId, rideId):
        # fcm notify driver about ride
        pass

    def notify_user(self, userId, driverObj):
        # fcm notify user about ride
        pass
