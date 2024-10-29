from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddCustomerForm, AddAgentForm
from .models import Customer, Agent

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


def agent_list(request):
    if request.user.is_authenticated:
        agents = Agent.objects.all()
        return render(request, 'agent_list.html', {'agents': agents})
    else:
        messages.success(request, "Login to view agents")
        return redirect('home')

def agent_customer(request, pk):
    if request.user.is_authenticated:
        agent = Agent.objects.get(id=pk)
        customers = Customer.objects.filter(agent=agent)
        return render(request, 'agent_customers.html', {'agent': agent, 'customers':customers})
    else:
        messages.success(request, "Login to view this page")
        return redirect('home')

def add_agent(request):
    form = AddAgentForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                if not Agent.objects.filter(user=request.user).exists():
                    add_record = form.save(commit=False)
                    add_record.user = request.user
                    add_record.save()
                    messages.success(request, "Agent added..")
                    return redirect('agent')
        return render(request, 'add_agent.html', {'form':form})
    else:
        messages.success(request, "Login to add agent..")
        return redirect('home')

def agent_detail(request, pk):
    if request.user.is_authenticated:
        # Records for agents chekups
        agent = Agent.objects.get(id=pk)
        return render(request, 'agent_detail.html', {'agent':agent})
    else:
        messages.success(request, "Login to view the page..")
        return redirect('home')

def agent_delete(request, pk):
    if request.user.is_authenticated:
        delete_record = Agent.objects.get(id=pk)
        delete_record.delete()
        messages.success(request, "Record Deleted")
        return redirect('agent_list')
    else:
        messages.success(request, "Login to delete records..")
        return redirect('home')

def agent_update(request, pk):
    if request.user.is_authenticated:
        current_agent = Agent.objects.get(id=pk)
        form = AddAgentForm(request.POST or None, instance=current_agent)
        if form.is_valid():
            form.save()
            messages.success(request, "Record updated!")
            return redirect('agent')
        return render(request, 'agent_update.html', {'form':form})
    else:
        messages.success(request, "Login to update..")
        return redirect('home')