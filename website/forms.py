# =--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-
# 
# Created by: CMPT370 Group 28 - Harrison H., Bailey G., Dan B., Tanisha, Demi B. and Mohammed O
# For use by: University of Saskatchewan, and MacDon Industries
# Project Information: Vehicle management system, allowing for tracking of trips taken from company vehicles by employees
#
# =--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-

from django import forms
from django.forms import ModelForm
from .models import Vehicle
from .models import Expense, LicensePlate, Vehicle 
from datetime import date 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User as Users

class LicensePlateForm(forms.ModelForm):
    class Meta:
        model = LicensePlate
        fields = ['plateID']

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = Users
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class EditUserForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = Users
        fields = ('username', 'first_name', 'last_name', 'email')

class FilterForm(forms.Form):
    FILTER_CHOICES = (
        ('license_plate', 'License_Plate'),
        ('brand', 'Brand'),
        ('active', 'Active'),
        ('kilometers', 'Kilometers'),
        ('employee', 'Employee'),
        ('vin', 'VIN'),
        ('all', 'All')
    )

    filter_by = forms.ChoiceField(choices=FILTER_CHOICES)

class LoginForm(forms.Form):
    FILTER_CHOICES = (
        ('username', 'username'),
        ('password', 'password')
    )

    filter_by_login = forms.ChoiceField(choices=FILTER_CHOICES)


class FilterFormUser(forms.Form):
    FILTER_CHOICES = (
        ('fname', 'fname'),
        ('employeeID', 'employeeID'),
        ('manager', 'manager')
    )

    filter_by_user = forms.ChoiceField(choices=FILTER_CHOICES)

class Expenseform(ModelForm):
    class Meta:
        model = Expense 
        fields = ['shopName', 'date', 'repairType', 'amountCharged', 'LicensePlate', 'receipt']
        labels = {
            'shopeName':'Shop Name',
            'date':'Date',
            'repairType':'Repair',
            'amountCharged':'Cost',
            'receipt':'Picture of Receipt'
        }
        widgets = {
            'shopName':forms.TextInput(attrs={'class':'form-control','placeholder':'Example: Dealership'}),
            'date':forms.DateInput(attrs={'class':'form-control','type':'date','placeholder':'yyy-mm-dd' }),
            'repairType':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Example: Tire rotation'}),
            'amountCharged':forms.NumberInput(attrs={'class':'form-control', 'placeholder':'1234'}),
            'LicensePlate':forms.TextInput(attrs={'class':'form-control', 'placeholder':'XXXXXX'})
        }
