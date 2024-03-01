# =--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-
# 
# Created by: CMPT370 Group 28 - Harrison H., Bailey G., Dan B., Tanisha, Demi B. and Mohammed O
# For use by: University of Saskatchewan, and MacDon Industries
# Project Information: Vehicle management system, allowing for tracking of trips taken from company vehicles by employees
# V0.1.0 
#
# =--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-
# =--=-=-==-=- Imports =--==-=-=-=--==-
from .models import Vehicle, LicensePlate, Expense, Ticket, Trip, PersonalVehicle, Accident
from .forms import FilterForm, FilterFormUser, RegisterUserForm, LicensePlateForm
from functools import wraps

# =--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-
# --=-=-=-==-=-=- Django imports -=-==-=-=-=-=-=-
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User as Users
from django.db import IntegrityError

# =--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-
@login_required

def home(request):
    """Handling of the home page:
    Assigns user to a vehicle and updates the trip information
    Allows for a user to sign back in a vehicle, also updates trip information 
    """
    all_vehicles = Vehicle.objects.all
    all_users = Users.objects.all
    license_plates = LicensePlate.objects.all

    if request.method == "POST":
        try:
            #gather information from the post req, allowing for the information in the db to be updated 
            vehicle_lp = request.POST.getlist('updated_lp')
            updated_id = request.POST.getlist('changedEmployeeID')
            updated_destination = request.POST.getlist('updated_destination')
            status = request.POST.getlist('checkInOut')[0]

            new_trip = Trip(
                licensePlate    = LicensePlate.objects.get(id = vehicle_lp[0]), 
                location        = updated_destination[0],
                user            = updated_id[0],
                checkout        = request.POST.getlist('checkout_time')[0],
                tripType        = status, 
            )
            new_trip.save()
            # Update the vehicle db
            Vehicle.objects.filter(LicensePlate__plateID__contains = vehicle_lp[0]).update(assignedEmployee = updated_id[0], currentTrip = new_trip)
            if status == "Available":
                messages.success(request,("Sucessfully checked in vehicle"))
            else:
                messages.success(request,("Sucessfully checked out vehicle"))

            return redirect("vehicle")
        except (Vehicle.DoesNotExist):
            messages.success(request,("Uh oh! It looks like that is not a valid vehicle entry!"))
        except (Users.DoesNotExist):
            messages.success(request,("Uh oh! It looks like that is not a valid user entry!"))

    # Default page creation if a post req is not received
    return render(request, "home.html", {'vehicles_db':all_vehicles, 'user_db':all_users, 'lp_db': license_plates})

# =--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-
@login_required

def individual_vehicle(request, vehicle_id):
    """View the information for an individual vehicle:
    Shows the total vehicle description, expenses and all trips that have been taken
    """
    all_trips = Trip.objects.all()
    single_vehicle = Vehicle.objects.get(pk=vehicle_id)
    expense_all = Expense.objects.filter(LicensePlate=single_vehicle.LicensePlate)
    return render(request, "individual_vehicle.html", {'individual_vehicle': single_vehicle, 'expense_all' : expense_all,"all_trips": all_trips})

# =--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-
@login_required

def individual_user(request, user_id):
    """View all the information for an individual user:
    Shows the complete user information, assigned vehicles, and the tickets associated with the user
    """

    if user_id == "NONE":
        return redirect('vehicle')
    individual_user = Users.objects.get(username =user_id)
    vehicle_all = Vehicle.objects.all()
    tickets_all= Ticket.objects.all()
    return render(request, "individual_user.html", {'individual_user': individual_user, 'vehicle_all' : vehicle_all, 'ticket_db' : tickets_all})

# =--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-
@login_required

def search_vehicles(request):
    """Renders the search results from the search screen:
    Passed values from the users and the vehicles db, showing all matching cases from both databases
    """
    if request.method == 'POST':
        searched = request.POST['searched']
        vehicles = Vehicle.objects.filter(Q(assignedEmployee__contains=searched) | Q(LicensePlate__plateID__contains=searched) | Q(VIN__contains=searched) | Q(model__contains=searched) | Q(make__contains=searched) | Q(year__contains=searched) | Q(currentTrip__location__contains=searched))
        users = Users.objects.filter(Q(first_name__contains=searched) | Q(last_name__contains=searched) | Q(email__contains=searched) | Q(username__contains=searched))
        
        return render(request, "search_vehicles.html", {'searched':searched, 'vehicles':vehicles, 'users':users})
    else:
        return redirect(request, "search_vehicle.html", {})
    
# =--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-
@login_required

def add_user(request):
    """Create a new user:
    Creates a form for taking new user information, this is done through the Django.auth framework 
    If the form is not completed, the errors are displayed to the user
    """
    all_users = Users.objects.all
    license_plates = LicensePlate.objects.all
    if request.method == "POST":
        form = RegisterUserForm(request.POST or None)
      
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']        
            messages.success(request, ("Registration Success!"))
            return render(request, "register_user.html",{'form':form})
        else:
            messages.success(request, (form.errors))

    else:
        form = RegisterUserForm()
    return render(request, "register_user.html",{'form':form})

# =--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-
@login_required

def add_truck(request):
    """Create a new vehicle:
    Takes input from add_vehicle.html through a post req
    Creates a trip model, then assigns this trip model to the vehicle model
    """
    if request.user.is_superuser:

        license_plates = LicensePlate.objects.all
        all_users = Users.objects.all
        all_trips = Trip.objects.all

        # Check if vehicle_id is provided for editing
        # if vehicle_id:
        #     vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        # else:
        #     vehicle = None

        if request.method == "POST":
            new_license_plate = request.POST.getlist('assigned_license_plate')[0]
            # Create trip model
            new_trip = Trip(
                # assign values to the model
                licensePlate    = LicensePlate.objects.get(id = new_license_plate),
                location        = request.POST.getlist('currentTrip')[0],
                user            = request.POST.getlist('assignedEmployee')[0],
                tripType        = request.POST.getlist('checked_in')[0],

            )
            new_trip.save()

            new_vehicle = Vehicle(  
                #assign values to the model   
                assignedEmployee = request.POST.getlist('assignedEmployee')[0], 
                LicensePlate = LicensePlate.objects.get(id = new_license_plate), 
                VIN = request.POST.getlist('VIN')[0], 
                make = request.POST.getlist('make')[0], 
                model = request.POST.getlist('model')[0], 
                year = request.POST.getlist('year')[0], 
                kms = request.POST.getlist('kms')[0], 
                currentTrip = new_trip 
                )
            
            new_vehicle.save()
            # messages.success(request,("Successfully added to the Vehicle Database"))
            # if vehicle:
            #     messages.success(request, "Vehicle updated successfully.")
            # else:
            #     messages.success(request, "Successfully added to the Vehicle Database")
            return redirect("vehicle")

        else:
            # return render(request, "add_vehicle.html", { 'user_db':all_users, 'lp_db': license_plates})
            return render(request, "add_vehicle.html", {'user_db': all_users, 'lp_db': license_plates, 'vehicle': vehicle})
    else:
        messages.success(request,("You do not have access to this page!"))
        return redirect("home")

# =--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=
@login_required

def add_license_plate(request):
    """Create a license plate:
    License plates are the linking component of vehicles to users as they are mutually exclusive items
    """
    license_plates = LicensePlate.objects.all
    all_vehicles = Vehicle.objects.all

    if request.user.is_superuser:
        if request.method == "POST":
            form = LicensePlateForm(request.POST or None)
            if form.is_valid():
                form.save()
            else:
                messages.success(request,("There was an error in your form, please try again!"))

                return render(request, "add_license_plate.html", {})

            messages.success(request,("Successfully added the license plate!"))
            return redirect("add_truck")

        else:
            return render(request, "add_license_plate.html", {})
    else:
        messages.success(request,("You do not have access to this page!"))
        return redirect("home")

        


# =--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-
@login_required

def expense(request):
    """Create a new expense:
    Values are passed trough a POST req then read and a model is created from this information
    """
    all_vehicles = Vehicle.objects.all
    all_expenses = Expense.objects.all
    all_tickets = Ticket.objects.all
    all_users = Users.objects.all
    license_plates = LicensePlate.objects.all

    if request.method == "POST":
        vehicle_lp = request.POST.getlist('lp')[0]
        expenseShop    = request.POST.getlist('expense_shop')[0]
        expenseRepair     = request.POST.getlist('expense_repair')[0]
        expenseCost = request.POST.getlist('expense_cost')[0]
        expenseDate       = request.POST.getlist('date')[0]
        licensePlate     = LicensePlate.objects.get(id = vehicle_lp)
        expenseIMG        = request.POST.getlist('expenseIMG')[0]
        new_expense = Expense(           
            shopName            = expenseShop,
            repairType          = expenseRepair,
            date                = expenseDate,
            LicensePlate        = licensePlate,
            amountCharged       = expenseCost,
            receipt             = expenseIMG             
            )
        
        new_expense.save()
        messages.success(request,("Successfully added expense"))
        return redirect("display_expense")

    else:
        return render(request, "expense.html",{'vehicles_db':all_vehicles, 'expense_db':all_expenses, 'ticket_db':all_tickets, 'user_db':all_users, 'lp_db': license_plates})


# =--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-
@login_required

def display_expenses(request):
    """Display the expense information:
    Renders the page to display the expense information
    """
    data = Expense.objects.all
    personal_vehicle = PersonalVehicle.objects.all
    return render(request, "display_expenses.html",{'expenses':data, "personal_vehicle":personal_vehicle})

# =--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-
@login_required

def vehicle(request):
    """ Display the information from the vehicle db:
    Also handles the filtering function to allow for the results to be filtered by: employee, vehicle brand and vin
    """
    # Grab all the vehicle database
    all_vehicles = Vehicle.objects.all
    license_plate = LicensePlate.objects.all
    #Query the vehicle model for assigned employees
    vehicle_employees = Vehicle.objects.order_by('assignedEmployee')
    #Query the vehicle model for car brand
    vehicle_brand = Vehicle.objects.order_by('make')
    #Query the vehicle model for VIN
    vehicle_vin = Vehicle.objects.order_by('VIN')

    if request.method == "POST":
        form = FilterForm(request.POST or None)
        filter_choice = ''
        if form.is_valid():
            filter_choice = form.cleaned_data.get('filter_by')
            if filter_choice == "employee":
                return render(request, "vehicle.html",{'vehicles_db': vehicle_employees })
     
            elif filter_choice == "brand":
                return render(request, "vehicle.html",{'vehicles_db': vehicle_brand })
                        
            elif filter_choice == "vin":
                return render(request, "vehicle.html",{'vehicles_db': vehicle_vin, "lp_db": license_plate})
            
            elif filter_choice == "all":
                return render(request, "vehicle.html",{'vehicles_db': all_vehicles })
            
            else:
                return render(request, "vehicle.html",{'vehicles_db':all_vehicles}) 

        else:

            return render(request, "vehicle.html",{'vehicles_db':all_vehicles})    
        
    else:
        return render(request, "vehicle.html",{'vehicles_db':all_vehicles})

# =--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-
@login_required

def user(request):
    """Display the users from the user db:
    Also handles the filtering function to allow for the results to be filtered by: first name, username or manager 
    """
    # Grab all the users database
    all_users = Users.objects.all
    #Query the vehicle model for first name
    user_fname = Users.objects.order_by('first_name')
    #Query the vehicle model for employee ID
    user_ID = Users.objects.order_by('username')
    #Query the vehicle model for manger
    user_manager = Users.objects.order_by('is_superuser')

    if request.method == "POST":
        form = FilterFormUser(request.POST or None)
        filter_choice = ''
        if form.is_valid():
            filter_choice = form.cleaned_data.get('filter_by_user')
            if filter_choice == "fname":
                return render(request, "user.html",{'user_db': user_fname })
            elif filter_choice == "employeeID":
                return render(request, "user.html",{'user_db': user_ID })
            elif filter_choice == "manager":
                return render(request, "user.html",{'user_db': user_manager })
            else:
                 return render(request, "user.html",{'user_db':all_users})
            

        else:
             return render(request, "user.html",{'user_db':all_users}) 
    else:    
        return render(request, "user.html",{'user_db':all_users})

# =--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-

def login_user(request):
    """Handles the user login:
    Follows the framework from Django.auth, redirecting the user to the homepage upon successful login
    """
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #redircet to success
            messages.success(request, ("Welcome!"))
            response =  redirect("home")
            #setting cookies
            response.set_cookie('username', username)
            response.set_cookie('login_status', True)
            return response
        else:
            try:
                Users.objects.get(username = username)
            # if the username does not exist, redirect to registration page
            except (Users.DoesNotExist):
               messages.success(request, ("User not found, please register"))
               return render(request, "register_user.html",{})
             
            #reload the screen with popup 
            messages.success(request, ("Password incorrect"))
            return render(request, "login.html",{})
    else:
        return render(request, "login.html",{})
    
    
# =--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-
@login_required

def logout_user(request):
    """Logout the user from their current session: 
    Follows the Django.auth framework, signing the current user out of the session, and bringing them back to the login screen
    """
    logout(request)
    messages.success(request, ("You have logged out."))
    response= redirect("login_user")
    #deleting cookies
    response.delete_cookie('username')
    response.delete_cookie('login_status')
    return response

# =--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-

def register_user(request):
    """Register a new user:
    Creates a form for taking new user information, this is done through the Django.auth framework 
    If the form is not completed, the errors are displayed to the user
    Differs from create_user as this is available when the user is not logged in
    """
    if request.method == "POST":
        form = RegisterUserForm(request.POST or None)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Registration Success!"))
            return redirect("home")

    else:
        form = RegisterUserForm()
    return render(request, "register_user.html",{'form':form})

# =--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-
@login_required

def admin_approval(request):
    """admin approval of expenses:
    Allows for admin's/manager's to approve expenses, tickets and update the db accordingly
    """
    pv_count = PersonalVehicle.objects.all().count()
    expense_count = Expense.objects.all().count()
    vehicle_count = Vehicle.objects.all().count()
    user_count = Users.objects.all().count() # this is just the user count, not the registered users

    expense_list = Expense.objects.all().order_by('-date')
    pv = PersonalVehicle.objects.all().order_by('-date')

    if request.user.is_superuser:
        if request.method == "POST":
            id_list = request.POST.getlist('boxes')
            pv_list = request.POST.getlist('pvboxes')

            #uncheck expenses
            expense_list.update(approved=False)
            pv.update(approved= False)

            #update db
            for x in id_list:
                Expense.objects.filter(pk=int(x)).update(approved=True)
            for x in pv_list:
                PersonalVehicle.objects.filter(pk=int(x)).update(approved=True)

            messages.success(request,("Added approvals."))
            return render(request, "display_expenses.html",{"expenses":expense_list, 'personal_vehicle':pv})

        else:
            return render(request, "admin_approval.html",{"expenses":expense_list, "pv":pv, "expense_count":expense_count,
                                                          "vehicle_count":vehicle_count, "user_count":user_count, "pv_count":pv_count})
    else:
        messages.success(request,("Must be an admin to view this page."))
        return redirect("home")
    
# =--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-
@login_required

def profile(request):
    """Display the logged in users information:
    This includes the vehciles assigned to them, and the tickets that are assigned to them
    """
    all_vehicles = Vehicle.objects.all
    all_tickets = Ticket.objects.all
    all_pv = PersonalVehicle.objects.all
    all_acc = Accident.objects.all
    return render(request, "profile.html",{'vehicle_db':all_vehicles, 'ticket_db':all_tickets, 'personal_vehicle':all_pv, 'accidents': all_acc})

# =--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-
@login_required

def view_databases(request):
    """View all the databases:
    This allows for admin users to view all the data in the databases
    Each value is able to be clicked to redirect to edit the database entries
    """
    # Grab all the vehicle database
    all_vehicles = Vehicle.objects.all
    # Grab all the users database
    all_users = Users.objects.all
    # Grab all the tickets database
    all_tickets = Ticket.objects.all
    # Grab all the expenses database
    all_expenses = Expense.objects.all

    return render(request, "view_databases.html",{'vehicle_db':all_vehicles, 'user_db': all_users, 'ticket_db': all_tickets, 'expense_db': all_expenses} )

# =--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-
@login_required

def edit_users(request, toUpdateUsername):
    """Edit a user:
    Creates a form for editing existing user information
    Gets form information from POST req to populate the model information
    """
    if request.user.is_superuser:
        all_users = Users.objects.all
        try: 
            updateUser = Users.objects.get(username = toUpdateUsername) #username, email, first name, last name
        except (Users.DoesNotExist):
            messages.success(request, "Uh oh! That user does not exist!")
            return redirect("view_databases")
        
        if request.method =="POST":
            try:
                update_fname = request.POST.getlist("first_name")[0]
                update_lname = request.POST.getlist("last_name")[0]
                update_email = request.POST.getlist("email")[0]
                update_uname = request.POST.getlist("username")[0]
                Users.objects.filter(username__contains = toUpdateUsername).update(first_name = update_fname, last_name = update_lname, email = update_email, username = update_uname)

                return redirect("view_databases")
            except (IntegrityError):
                messages.success(request, "Uh oh! That username is already taken, please enter a different username!")
                return render(request, "edit_users.html", {'user': updateUser})

        # if not post req
        else:
            return render(request, "edit_users.html", {'user': updateUser})

# =--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-
@login_required

def delete(request, toUpdate):
    """Deletes a user, vehicle, expense and ticket:
    deletes an  existing user, vehicle, expense and ticket information
    """
    if request.user.is_superuser:
        try: 
            deleteEntry = Users.objects.get(username = toUpdate) #username, email, first name, last name
            entryType = "Users"
        except (Users.DoesNotExist):
            try:
                deleteEntry = Vehicle.objects.get(VIN = toUpdate)
                print("I think im a vehicle")
                entryType = "Vehicles"

            except (Vehicle.DoesNotExist):
                try:
                    deleteEntry = Expense.objects.get(repairType = toUpdate)
                    entryType = "Expenses"

                except (Expense.DoesNotExist):
                    try:
                        deleteEntry = Ticket.objects.get(ticketType = toUpdate)
                        entryType = "Tickets"

                    except (Ticket.DoesNotExist):
                        messages.success(request, "Uh oh! That entry does not exist!")
                        return redirect("view_databases")
            

        if request.method =="POST":
            confirm = request.POST.getlist("confirm")[0]
            if confirm == "confirmed":
                if entryType == "Users":
                    entry = Users.objects.get(username__contains = toUpdate)
                    try: 
                        PersonalVehicle.objects.get(assignedEmployee = entry).update(assignedEmployee = None ) 
                    except:
                        None
                    try: 
                        Accident.objects.get(assignedEmployee = entry).update(assignedEmployee = None ) 
                    except:
                        None
                    try: 
                        Ticket.objects.get(assignedEmployee = entry).update(assignedEmployee = None ) 
                    except:
                        None
                    Users.objects.get(username__contains = toUpdate).delete()
                elif entryType == "Vehicles":
                    Vehicle.objects.get(VIN__contains = toUpdate).delete()
                elif entryType == "Expenses":
                    Expense.objects.get(repairType__contains = toUpdate).delete()
                elif entryType == "Tickets":
                    Ticket.objects.get(ticketType__contains = toUpdate).delete()
                
                messages.success(request, "Deleted")
                return redirect("view_databases")
            else:
                return redirect("view_databases")
        # if not post req
        else:
            return render(request, "delete.html", {'entry': entryType, "specific":deleteEntry})
# =--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-
@login_required
def edit_truck(request, toUpdateTruck):
    """Edit a truck:
    Creates a form for editing existing truck information
    Gets form information from POST req to populate the model information
    """
    if request.user.is_superuser:
        all_vehicles = Vehicle.objects.all
        all_lp = LicensePlate.objects.all
        try: 
            updateTruck = Vehicle.objects.get(id = toUpdateTruck) #make, model, vin, kms, lp
        except (Vehicle.DoesNotExist):
            messages.success(request, "Uh oh! That vehicle does not exist!")
            return redirect("view_databases")
        
        if request.method =="POST":
            update_make = request.POST.getlist("make")[0]
            update_model = request.POST.getlist("model")[0]
            update_LicensePlate = request.POST.getlist("updated_license_plate")[0]
            update_year = request.POST.getlist("year")[0]
            update_kms = request.POST.getlist("kms")[0]
            update_VIN = request.POST.getlist("VIN")[0]
            Vehicle.objects.filter(id__contains = toUpdateTruck).update(make = update_make, model = update_model, LicensePlate = update_LicensePlate, year = update_year, kms = update_kms, VIN = update_VIN)

            return redirect("view_databases")
            

        # if not post req
        else:
            return render(request, "edit_truck.html", {'truck': updateTruck, 'lp_db':all_lp})
        
# =--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-
@login_required

def edit_expenses(request, toUpdateExpense):
    """Edit an expense:
    Creates a form for editing existing expense information
    Gets form information from POST req to populate the model information
    """
    if request.user.is_superuser:
        all_expenses = Expense.objects.all
        all_users = Users.objects.all 
        all_lp = LicensePlate.objects.all
        try: 
            updateExpense = Expense.objects.get(id = toUpdateExpense) #shop, date, repair, cost
        except (Expense.DoesNotExist):
            messages.success(request, "Uh oh! That expense does not exist!")
            return redirect("view_databases")
        
        if request.method =="POST":
            lp = request.POST.getlist("update_lp")[0]
            update_eshop = request.POST.getlist("expense_shop")[0]
            update_edate = request.POST.getlist("date")[0]
            update_erepair = request.POST.getlist("expense_repair")[0]
            update_ecost = request.POST.getlist("expense_cost")[0]
            update_LicensePlate = LicensePlate.objects.get(id = lp)
            Expense.objects.filter(id__contains = toUpdateExpense).update(shopName = update_eshop, date = update_edate, repairType = update_erepair, amountCharged = update_ecost, LicensePlate = update_LicensePlate)

            return redirect("view_databases")
            

        # if not post req
        else:
            return render(request, "edit_expenses.html", {'expense': updateExpense, 'lp_db':all_lp, 'user_db':all_users})
        
# =--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-
@login_required

def edit_tickets(request, toUpdateTicket):
    """Edit a ticket:
    Creates a form for editing existing ticket information
    Gets form information from POST req to populate the model information
    """
    if request.user.is_superuser:
        all_tickets = Ticket.objects.all
        all_users = Users.objects.all 
        all_lp = LicensePlate.objects.all
        try: 
            updateTicket = Ticket.objects.get(id = toUpdateTicket) #ticket type, cost, date, lp, emploee ID
        except (Ticket.DoesNotExist):
            messages.success(request, "Uh oh! That ticket does not exist!")
            return redirect("view_databases")
        
        if request.method =="POST":
            lp = request.POST.getlist("updated_lp")[0]
            update_ttype = request.POST.getlist("ticket_type")[0]
            update_tcost = request.POST.getlist("ticket_cost")[0]
            update_date = request.POST.getlist("date")[0]
            update_LicensePlate = LicensePlate.objects.get(id = lp)
            update_eID = request.POST.getlist("employeeID")[0]

            Ticket.objects.filter(id__contains = toUpdateTicket).update(ticketType = update_ttype, ticketAmt = update_tcost, date = update_date, LicensePlate = update_LicensePlate, assignedEmployee = update_eID)

            return redirect("view_databases")

        # if not post req
        else:
            return render(request, "edit_tickets.html", {'ticket': updateTicket, 'lp_db':all_lp, 'user_db':all_users})
# =--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-
@login_required

def tickets(request):
    """Create a new ticket:
    Creates a form for taking new ticket information
    Gets form information from POST req to populate the model information
    """
    all_vehicles = Vehicle.objects.all
    all_expenses = Expense.objects.all
    all_tickets = Ticket.objects.all
    all_users = Users.objects.all
    license_plates = LicensePlate.objects.all

    if request.method == "POST":
        vehicle_lp       = request.POST.getlist('lp')[0]
        employee_id      = request.POST.getlist('employeeID')[0]
        newticketType    = request.POST.getlist('ticket_type')[0]
        ticketAmount     = request.POST.getlist('ticket_cost')[0]
        ticketDate       = request.POST.getlist('date')[0]
        licensePlate     = LicensePlate.objects.get(id = vehicle_lp)
        employee         = Users.objects.get(id = employee_id)
        ticketIMG        = request.POST.getlist('ticketIMG')[0]
        new_ticket = Ticket(           
            ticketType          = newticketType,
            ticketAmt           = ticketAmount,
            date                = ticketDate,
            LicensePlate        = licensePlate,
            assignedEmployee    = employee,
            ticket              = ticketIMG             

            )

        new_ticket.save()
        messages.success(request,("Successfully added ticket"))
        return redirect("tickets")


    else:
        return render(request, "tickets.html",{'vehicles_db':all_vehicles, 'expense_db':all_expenses, 'ticket_db':all_tickets, 'user_db':all_users, 'lp_db': license_plates})

# =--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-
@login_required

def personal_vehicle(request):
    """Create a new expense:
    Values are passed trough a POST req then read and a model is created from this information
    """
    all_vehicles = Vehicle.objects.all
    all_expenses = Expense.objects.all
    all_tickets = Ticket.objects.all
    all_users = Users.objects.all
    license_plates = LicensePlate.objects.all

    if request.method == "POST":
        assignedEmployee    = request.POST.getlist('assignedEmployee')[0]
        tripReason          = request.POST.getlist('reason')[0]
        kmTravel            = request.POST.getlist('km_travelled')[0]
        tripDate            = request.POST.getlist('date')[0]
       
        new_pv = PersonalVehicle(           
            km                        = kmTravel,
            assignedEmployee          = Users.objects.get(username = assignedEmployee),
            date                      = tripDate,
            reason                    = tripReason,
            )
        
        new_pv.save()
        messages.success(request,("Successfully added personal vehicle request"))
        return redirect("display_expense")

    else:
        return render(request, "personal_vehicle.html",{'user_db':all_users})
    
# =--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-
@login_required

def accidents(request):
    """Create a new expense:
    Values are passed trough a POST req then read and a model is created from this information
    """
    all_vehicles = Vehicle.objects.all
    all_expenses = Expense.objects.all
    all_tickets = Ticket.objects.all
    all_users = Users.objects.all
    license_plates = LicensePlate.objects.all
    all_accidents = Accident.objects.all

    if request.method == "POST":
        acc_location            = request.POST.getlist('location')[0]
        acc_fault               = request.POST.getlist('fault')[0]
        acc_date                = request.POST.getlist('date')[0]
        acc_licensePlate        = request.POST.getlist('lp')[0]
        acc_assignedEmployee    = request.POST.getlist('employeeID')[0]
        acc_picture             = request.POST.getlist('picture')[0]
       
        new_acc = Accident(           
            location                  = acc_location,
            fault                     = acc_fault,
            date                      = acc_date,
            LicensePlate              = LicensePlate.objects.get(id = acc_licensePlate),
            assignedEmployee          = Users.objects.get(username = acc_assignedEmployee),
            picture                   = acc_picture
            )
        
        new_acc.save()
        messages.success(request,("Successfully added accident"))
        return redirect("display_accidents")

    else:
        return render(request, "accident.html",{'user_db':all_users, 'all_accidents':all_accidents, 'vehicle_db':all_vehicles, 'lp_db':license_plates})
    
# =--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-=--=-==-=-=-=-=-=-=-
@login_required

def display_accidents(request):
    """Display the expense information:
    Renders the page to display the expense information
    """
    data = Accident.objects.all
    
    return render(request, "display_accidents.html",{'accidents':data})
