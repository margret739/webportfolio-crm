from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddCustomerForm
from .models import Customer

# Create your views here.
def home(request):
    customers = Customer.objects.all()

    # check log in
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password')
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')
        else:
            messages.success(request, "Error logging in, Please try again...")
            return redirect('home')
    else:
        return render(request, 'home.html', {'customers':customers})



def logout_user(request):
    logout(request)
    messages.success(request, "Logging out..")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # authenticating and logging in
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration Successfull!")
            return redirect('home')

    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
        
    return render(request, 'register.html', {'form':form}) 


def record_customer(request, pk):
    if request.user.is_authenticated:
        # Records for customer chekups
        record_customer = Customer.objects.get(id=pk)
        return render(request, 'customer.html', {'record_customer':record_customer})
    else:
        messages.success(request, "Login to view the page..")
        return redirect('home')

def delete_customer(request, pk):
    if request.user.is_authenticated:
        delete_record = Customer.objects.get(id=pk)
        delete_record.delete()
        messages.success(request, "Record Deleted")
        return redirect('home')
    else:
        messages.success(request, "Login to delete records..")
        return redirect('home')


def add_customer(request):
    form = AddCustomerForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Customer added..")
                return redirect('home')
        return render(request, 'add_customer.html', {'form':form})
    else:
        messages.success(request, "Login to add customer..")
        return redirect('home')


def update_customer(request, pk):
    if request.user.is_authenticated:
        current_customer = Customer.objects.get(id=pk)
        form = AddCustomerForm(request.POST or None, instance=current_customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Record updated!")
            return redirect('home')
        return render(request, 'update_customer.html', {'form':form})
    else:
        messages.success(request, "Login to update..")
        return redirect('home')
