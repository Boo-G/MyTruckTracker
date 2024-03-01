# =--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-
# 
# Created by: CMPT370 Group 28 - Harrison H., Bailey G., Dan B., Tanisha, Demi B. and Mohammed O
# For use by: University of Saskatchewan, and MacDon Industries
# Project Information: Vehicle management system, allowing for tracking of trips taken from company vehicles by employees
#
# =--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-

from django.contrib import admin
from .models import Vehicle 
from .models import Expense 
from .models import LicensePlate
from .models import Trip
from .models import Ticket
from .models import PersonalVehicle
from .models import Accident

# Register your models here.
admin.site.register(Vehicle)
admin.site.register(Expense)
admin.site.register(LicensePlate)
admin.site.register(Trip)
admin.site.register(Ticket)
admin.site.register(PersonalVehicle)
admin.site.register(Accident)
