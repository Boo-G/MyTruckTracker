# =--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-
# 
# Created by: CMPT370 Group 28 - Harrison H., Bailey G., Dan B., Tanisha, Demi B. and Mohammed O
# For use by: University of Saskatchewan, and MacDon Industries
# Project Information: Vehicle management system, allowing for tracking of trips taken from company vehicles by employees
#
# =--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-

from django.db import models
from django.db.models.fields.files import ImageField
from django import forms
from datetime import date
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User as Users

# Create your models here.
# Database Models and ORM

class LicensePlate(models.Model):
    plateID=models.CharField(max_length=6)

    def __str__(self):
        return str(self.plateID) 

class Accident(models.Model):
    location            = models.CharField(max_length=100)
    fault               = models.CharField(max_length=100)
    date                = models.DateField('Ticket Date')
    LicensePlate        = models.ForeignKey(LicensePlate, blank=True, null=True, on_delete=models.DO_NOTHING)
    assignedEmployee    = models.ForeignKey(Users, blank=True, null=True, on_delete=models.DO_NOTHING)
    picture              = models.ImageField(null=True, blank=True, upload_to="images/ticket")
   
    def __str__(self):
        return str(self.assignedEmployee) + ' Accident ' + ' | '+self.location  + ' | ' + str(self.date)

class Ticket(models.Model):
    ticketType = models.CharField(max_length=100)
    ticketAmt = models.CharField(max_length=100)
    date = models.DateField('Ticket Date')
    LicensePlate = models.ForeignKey(LicensePlate, blank=True, null=True, on_delete=models.DO_NOTHING)
    assignedEmployee = models.ForeignKey(Users, blank=True, null=True, on_delete=models.DO_NOTHING)
    ticket = models.ImageField(null=True, blank=True, upload_to="images/ticket")
   
    def __str__(self):
        return self.ticketType + ' | ' + str(self.assignedEmployee) + ' | ' + str(self.date)

class Trip(models.Model):
    licensePlate    = models.ForeignKey(LicensePlate, blank=True, null=True, on_delete=models.DO_NOTHING)
    tripType        = models.CharField(max_length=10, null = True)
    location        = models.CharField(max_length=32)
    checkout        = models.DateTimeField(null = True)
    checkin         = models.DateTimeField(null = True)
    user            = models.CharField(max_length=6, null = True)

    def __str__(self):
        return str(self.licensePlate) + " | " + str(self.location) + " | " + str(self.user) 


# vehicle database
class Vehicle(models.Model):
    assignedEmployee = models.CharField(max_length=25)
    LicensePlate = models.ForeignKey(LicensePlate, blank=True, null=True, on_delete=models.DO_NOTHING)
    VIN = models.CharField(max_length=17)
    make = models.CharField(max_length=10)
    model = models.CharField(max_length=10)
    year = models.CharField(max_length=4)
    kms = models.CharField(max_length=9)
    receipt = models.ImageField(upload_to="media/images/service", blank=True)            
    currentTrip = models.ForeignKey(Trip, blank=True, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.assignedEmployee + ' - ' + str(self.LicensePlate) + ' - '+ self.model

class Expense(models.Model):
    shopName = models.CharField(max_length=100)
    date =  models.DateField('Expense Date')
    repairType = models.CharField(max_length=100)
    amountCharged = models.DecimalField(max_digits=15, decimal_places=2)
    LicensePlate = models.ForeignKey(LicensePlate, blank=True, null=True, on_delete=models.DO_NOTHING)
    receipt = models.ImageField(upload_to="media/images/service") 
    approved = models.BooleanField("Approved", default=False)

    def __str__(self):
        return str(self.LicensePlate) + ' | ' + self.repairType + " | " + self.shopName  

class PersonalVehicle(models.Model):
    km               = models.CharField(max_length=8)
    assignedEmployee = models.ForeignKey(Users, blank=True, null=True, on_delete=models.DO_NOTHING)
    date             = models.DateField(null = True)
    approved         = models.BooleanField("Approved", default=False)
    reason           = models.CharField(max_length=100)

    def __str__(self):
        return  str(self.assignedEmployee)  + " personal vehicle trip for: " + self.reason 