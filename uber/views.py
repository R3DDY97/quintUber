import json

from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .service import Driver_Service, Ride_Service, memory_data


def parse_req(req):
    return json.loads(request.body.decode())

@cache_page(60 * 15)
def driver_list(request):
    if request.method == 'GET':
        drivers = memory_data.get_drivers_list()
        if drivers:
            return JsonResponse({"success": True, "data": drivers}, status=200)
        return JsonResponse({"success": False}, status=500)
    return JsonResponse({"success": False, "message": "method not allowed"}, status=405)

@cache_page(60 * 15)
def display_cars(request):
    if request.method == 'GET':
        return render(request, "uber/cars.html")
    return JsonResponse({"success": False, "message": "method not allowed"}, status=405)


@csrf_exempt
def request_ride(request):
    if request.method == "POST":
        data = parse_req(request)
        if "userId" in data and "location" in data:
            userId = data["userId"]
            location = data["location"]
            cab_color = data.get("cab_color", "white")

            driver_service = Driver_Service(userId, location, cab_color)
            ride_data = driver_service.process_ride_request()
            if ride_data:
                return JsonResponse(ride_data, status=200)
            return JsonResponse({"success": False}, status=500)
        else:
            return JsonResponse({"success": False, "message": "missing userId, location"}, status=400)
    return JsonResponse({"success": False, "message": "method not allowed"},  status=405)

@csrf_exempt
def accept_ride(request):
    if request.method == "POST":
        data = parse_req(request)
        if "rideId" in data and "driverId" in data:
            rideId = data["rideId"]
            driverId = data["driverId"]
            ride = Ride_Service(rideId)
            accept_response = ride.ride_accepted()
            if accept_response:
                return JsonResponse({"success": True}, status=200)
            return JsonResponse({"success": False}, status=500)
        else:
            return JsonResponse({"success": False, "message": "missing rideId, driverId"}, status=400)
    return JsonResponse({"success": False, "message": "method not allowed"}, status=405)


@csrf_exempt
def start_ride(request):
    if request.method == "POST":
        data = parse_req(request)
        if "rideId" in data and "location" in data:
            rideId = data["rideId"]
            start_location = data["location"]
            ride = Ride_Service(rideId)
            start_response = ride.ride_started(start_location)
            if start_response:
                return JsonResponse({"success": True}, status=200)
            return JsonResponse({"success": False}, status=500)
        else:
            return JsonResponse({"success": False, "message": "missing rideId, location"}, status=400)
    return JsonResponse({"success": False, "message": "method not allowed"}, status=405)

@csrf_exempt
def end_ride(request):
    if request.method == "POST":
        data = parse_req(request)
        if "rideId" in data and "location" in data:
            rideId = data["rideId"]
            destination_location = data["location"]
            ride = Ride_Service(rideId, destination_location)
            end_response = ride.ride_ended()
            if end_response:
                return JsonResponse({"success": True, data: end_response}, status=200)
            return JsonResponse({"success": False}, status=500)
        else:
            return JsonResponse({"success": False, "message": "missing rideId, location"}, status=400)
    return JsonResponse({"success": False, "message": "method not allowed"}, status=405)
