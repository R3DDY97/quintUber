from django.urls import path
from . import views


urlpatterns = [
    path("create/", views.request_ride, name="request_ride"),
    path("accept/", views.accept_ride, name="accept_ride"),
    path("start/", views.start_ride, name="start_ride"),
    path("end/", views.end_ride, name="end_ride"),


]
