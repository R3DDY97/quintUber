from django.db import models
from django.utils import timezone


class User(models.Model):
    user_id = models.AutoField(primary_key = True)
    phone = models.CharField(unique=True, max_length = 10)
    name = models.CharField(max_length = 50)
    age = models.CharField(max_length = 50)
    gender = models.CharField(max_length = 50)
    country = models.CharField(max_length = 50)
    home = models.CharField(max_length = 50, blank = True)
    home_lat = models.FloatField(null = True)
    home_long = models.FloatField(null = True)
    work = models.CharField(max_length = 50, blank = True)
    work_lat = models.FloatField(null = True)
    work_long = models.FloatField(null = True)

class Driver(models.Model):
    driver_id = models.AutoField(primary_key = True)
    phone = models.CharField(unique=True, max_length = 10)
    name = models.CharField(max_length = 50)
    vehicle = models.CharField(max_length = 50)
    color = models.CharField(max_length=50)
    available = models.BooleanField(default = True)
    pos_lat = models.FloatField(blank = True)
    pos_long = models.FloatField(blank = True)
    gcm_id = models.CharField(max_length = 200, blank = True)
    license_plate = models.CharField(max_length = 10, blank = True)


class User_Ride(models.Model):
    ACCEPTED = 'A'
    CANCELLED = 'C'
    PENDING = 'P'
    ENDED = 'E'
    RIDING = 'R'
    RIDE_STATUS = [
        (ACCEPTED, 'Accepted'),
        (CANCELLED, 'Cancelled'),
        (PENDING, 'Pending'),
        (ENDED, 'Ended'),
        (RIDING, 'Riding'),
    ]
    ride_id = models.CharField(primary_key = True)
    user_id = models.ForeignKey(User)
    driver_id = models.ForeignKey(Driver)
    start_time = models.DateTimeField(null = True)
    end_time = models.DateTimeField(null = True)
    ride_state =  models.CharField(choices=RIDE_STATUS, default=PENDING)
    initial_lat = models.FloatField(null = True)
    initial_long = models.FloatField(null = True)
    final_lat = models.FloatField(null = True)
    final_long = models.FloatField(null = True)
    distance = models.DecimalField(max_digits = 5, decimal_places = 1, null = True)
    travel_time = models.CharField(max_length = 10, blank = True)
    price = models.IntegerField(null = True)
