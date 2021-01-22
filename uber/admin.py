from django.contrib import admin

# Register your models here.
from .models import User, Driver, User_Ride, Pending_Ride

admin.site.register(User)
admin.site.register(Driver)
admin.site.register(User_Ride)
admin.site.register(Pending_Ride)
