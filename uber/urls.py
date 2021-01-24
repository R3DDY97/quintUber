from django.urls import path
from . import views


urlpatterns = [
    path("create/", views.request_ride, name="request_ride"),
    path("accept/", views.accept_ride, name="accept_ride"),
    path("start/", views.start_ride, name="start_ride"),
    path("end/", views.end_ride, name="end_ride"),
    path("drivers/", views.driver_list, name="drivers_list"),
    path("cars/", views.display_cars, name="drivers_list"),


]
