import json
from uuid import uuid4
from datetime import datetime

from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse, QueryDict

from .models import  User, Driver, Pending_Ride, User_Ride
from .service import Ride_Service, Ride,  Push_Notification


def parse_req(req):
    return json.loads(request.body.decode())

def request_ride(request):
    if request.method == "POST":
        data = parse_req(request)
        userId = data.userId
        location = data.location
        cab_color = data.cab_color
        ride_service = Ride_Service(userId, location, cab_color)
        nearest_driver = ride_service.get_nearest_drivers()
        if nearest_driver:
            rideId = uuid4()
            user_ride_data = {"userId": userId, "driverId": driverId, ride_id: rideId, "ride_state": "Pending",
                              "initial_lat": location.latitude, "initial_long": location.longitude}
            User_Ride.objects.create(user_ride_data)
            Push_Notification.notify_driver(nearest_driver, rideId)
            return JsonResponse({success: False, message:"Processing Request"})
        return JsonResponse({success: False, message: "No Drivers Available now. Please try after sometime"})
    return JsonResponse({success: False, message: "method not allowed"})


def accept_ride(request):
    if request.method == "POST":
        data = parse_req(request)
        rideId = data.rideId
        ride = Ride(rideId)
        ride.ride_accepted()
        return JsonResponse({success: True, message: "OK"})
    return JsonResponse({success: False, message: "method not allowed"})



def start_ride(request):
    if request.method == "POST":
        data = parse_req(request)
        rideId = data.rideId
        location = data.location
        ride = Ride(rideId, location)
        ride.ride_started()
        return JsonResponse({success: True, message: "OK"})
    return JsonResponse({success: False, message: "method not allowed"})

def end_ride(request):
    if request.method == "POST":
        data = parse_req(request)
        rideId = data.rideId
        location = data.location
        ride = Ride(rideId, location)
        ride.ride_ended()
        return JsonResponse({success: True, message: "OK"})
    return JsonResponse({success: False, message: "method not allowed"})



def driver_list(request):
    if request.method == 'GET':
        drivers = Driver.objects.all()
        return JsonResponse({success: True, data: drivers})
    return JsonResponse({success: False, message: "method not allowed"})
