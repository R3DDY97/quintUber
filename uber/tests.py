from django.test import TestCase
from uber.service import Driver_Service, Ride_Service, Distance_Service, memory_data

distance_service = Distance_Service()

class Distance_Service_Test(TestCase):
    def test_calc_distance_from_origin(self):
        '''calculates lat, longitude distance from origin 0, 0'''
        location = {"latitude": 13.750111, "longitude": 77.993896}
        distance = distance_service.calc_distance_from_origin(location)
        self.assertEqual(distance, 8806.26849)
        print("----------------------------------------------------------------------")
        print("calc_distance_from_origin working fine")
        print("----------------------------------------------------------------------")


    def test_calc_two_location_distance(self):
        location1 = {"latitude": 13.750111, "longitude": 77.993896}
        location2 = {"latitude": 13.739811, "longitude": 77.976425}

        distance = distance_service.calc_two_location_distance(location1, location2)
        self.assertEqual(distance, 2.26)
        print("calc_two_location_distance working fine")
        print("----------------------------------------------------------------------")




class Driver_Ride_Service_Test(TestCase):

    location = {"latitude": 13.740111, "longitude": 77.983896}
    cab_color = "white"
    userId = "5260e8f4-394a-415a-b509-874ac622a3b2"
    driver_service = Driver_Service(userId, location, cab_color)

    def test_get_nearest_driver(self):
        nearest_driver = self.driver_service.get_nearest_driver()
        self.assertEqual(nearest_driver, "05c777ba-aebb-405a-9e48-48d642eaf1f6")

        print("get_nearest_driver working fine")
        print("----------------------------------------------------------------------")


    def test_process_ride_request(self):
        process_response = self.driver_service.process_ride_request()
        self.assertEqual(process_response['success'], True)
        self.assertEqual(process_response['ride_data']['ride_state'], 'Pending')

        print("process_ride_request working fine")
        print("----------------------------------------------------------------------")

    def test_ride_accepted(self):
        process_response = self.driver_service.process_ride_request()
        rideId = process_response['ride_data']['ride_id']
        ride_service = Ride_Service(rideId)
        ride_accepted_response = ride_service.ride_accepted()
        is_driver_available = memory_data.DRIVER_DF.loc[memory_data.DRIVER_DF['driverId'] == ride_service.driverId, 'available'].values[0]
        self.assertEqual(ride_accepted_response, True)
        self.assertEqual(memory_data.RIDE_DATA[rideId]['ride_status'], "Accepted")
        self.assertEqual(is_driver_available, False)

        print("ride_accept working fine")
        print("----------------------------------------------------------------------")




    def test_ride_started(self):
        start_location = {"latitude": 13.740111, "longitude": 77.983896}
        process_response = self.driver_service.process_ride_request()
        rideId = process_response['ride_data']['ride_id']
        ride_service = Ride_Service(rideId)

        ride_started_response = ride_service.ride_started(start_location)

        self.assertEqual(ride_started_response, True)
        self.assertEqual(memory_data.RIDE_DATA[rideId]['ride_status'], "Started")
        self.assertEqual(memory_data.RIDE_DATA[rideId]['start_lat'], start_location['latitude'])
        self.assertEqual(memory_data.RIDE_DATA[rideId]['start_long'], start_location['longitude'])


        print("ride_started working fine")
        print("----------------------------------------------------------------------")

    def test_ride_ended(self):
        start_location = {"latitude": 13.740111, "longitude": 77.983896}
        destination_location = {"latitude": 13.8796, "longitude": 78.09886}
        process_response = self.driver_service.process_ride_request()
        rideId = process_response['ride_data']['ride_id']
        ride_service = Ride_Service(rideId)
        ride_started_response = ride_service.ride_started(start_location)
        ride_ended_response = ride_service.ride_ended(destination_location)

        self.assertEqual(ride_ended_response['success'], True)
        self.assertEqual(ride_ended_response['distance_travelled'], 20.1)
        self.assertEqual(ride_ended_response['price'], 40)
        self.assertEqual(memory_data.RIDE_DATA[rideId]['ride_status'], "Ended")
        self.assertEqual(memory_data.RIDE_DATA[rideId]['destination_lat'], destination_location['latitude'])
        self.assertEqual(memory_data.RIDE_DATA[rideId]['destination_long'], destination_location['longitude'])


        print("ride_ended working fine")
        print("----------------------------------------------------------------------")
