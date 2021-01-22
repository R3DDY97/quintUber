import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .service import Driver_Service, Ride_Service,  Push_Notification


def parse_req(req):
    return json.loads(request.body.decode())

def driver_list(request):
    if request.method == 'GET':
        drivers = Driver.objects.filter(available=True)
        return JsonResponse({success: True, data: drivers})
    return JsonResponse({success: False, message: "method not allowed"})


@csrf_exempt
def request_ride(request):
    if request.method == "POST":
        data = parse_req(request)
        userId = data.userId
        location = data.location
        cab_color = data.cab_color
        driver_service = Driver_Service(userId, location, cab_color)
        ride_data = driver_service.process_ride_request()
        return JsonResponse(ride_data)
    return JsonResponse({success: False, message: "method not allowed"})

@csrf_exempt
def accept_ride(request):
    if request.method == "POST":
        data = parse_req(request)
        rideId = data.rideId
        driverId = data.driverId
        ride = Ride_Service(rideId)
        ride.ride_accepted()
        return JsonResponse({success: True, message: "OK"})
    return JsonResponse({success: False, message: "method not allowed"})


@csrf_exempt
def start_ride(request):
    if request.method == "POST":
        data = parse_req(request)
        rideId = data.rideId
        start_location = data.location
        ride = Ride_Service(rideId)
        ride.ride_started(start_location)
        return JsonResponse({success: True, message: "OK"})
    return JsonResponse({success: False, message: "method not allowed"})

@csrf_exempt
def end_ride(request):
    if request.method == "POST":
        data = parse_req(request)
        rideId = data.rideId
        location = data.location
        ride = Ride_Service(rideId, location)
        ride.ride_ended()
        return JsonResponse({success: True, message: "OK"})
    return JsonResponse({success: False, message: "method not allowed"})
