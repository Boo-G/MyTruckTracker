# =--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-
# 
# Created by: CMPT370 Group 28 - Harrison H., Bailey G., Dan B., Tanisha, Demi B. and Mohammed O
# For use by: University of Saskatchewan, and MacDon Industries
# Project Information: Vehicle management system, allowing for tracking of trips taken from company vehicles by employees
#
# =--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-

from django.urls import path, re_path, include
from django.conf.urls import handler404
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [

    path("", views.home),

    path('login', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    path("home", views.home, name = "home"),
    
    path("vehicle", views.vehicle, name = "vehicle"),
    
    path("user", views.user),
    
    path("add_user", views.add_user),
    
    path("add_truck", views.add_truck, name = "add_truck"),

    path("expense", views.expense, name = 'expenses'),

    path("display_expenses", views.display_expenses, name = "display_expense"),

    path("login", views.login),

    path("tickets", views.tickets, name = "tickets"),

    path("search_vehicles", views.search_vehicles),
  
    path("individual_vehicle/<vehicle_id>", views.individual_vehicle),
    
    path("individual_user/<user_id>", views.individual_user),

    path("login_user", views.login_user, name = "login_user"),

    path("logout_user", views.logout_user),
    
    path("register_user", views.register_user),
    
    path("admin_approval", views.admin_approval),

    path("profile", views.profile),

    path("add_license_plate", views.add_license_plate),

    path("view_databases", views.view_databases, name = "view_databases"),

    path("edit_users/<toUpdateUsername>", views.edit_users),

    path("edit_truck/<toUpdateTruck>", views.edit_truck),

    path("delete/<toUpdate>", views.delete),

    path("edit_expenses/<toUpdateExpense>", views.edit_expenses),

    path("edit_tickets/<toUpdateTicket>", views.edit_tickets),

    path("accidents", views.accidents),

    path("display_accidents", views.display_accidents, name = "display_accidents"),
    
    path("personal_vehicle", views.personal_vehicle, name = "personal_vehicle")

]
