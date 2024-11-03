from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddCustomerForm, AddAgentForm, OrderForm
from .models import Customer, Agent, Product, Order

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        customers = Customer.objects.all()


        total_leads = Customer.objects.count()
        total_unassigned = Customer.objects.filter(agent__isnull=True).count()

        context = {
            'customers': customers,
            'total_leads': total_leads,
            'total_unassigned': total_unassigned,
        }
        return render(request, 'home.html', context)
    else:
        messages.error(request, "Please login to view dashboard.")
        return redirect('login') 

def login_user(request):
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
    return render(request, 'login.html')


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
        agents = Agent.objects.get(id=pk)
        customers = Customer.objects.filter(agent=agent)
        return render(request, 'agent_customer.html', {'agents': agents, 'customers':customers})
    else:
        messages.success(request, "Login to view this page")
        return redirect('home')

def add_agent(request):
    form = AddAgentForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                    add_record = form.save(commit=False)
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

def agent_delete(request, agent_pk):
    if request.user.is_authenticated:
        delete_record = Agent.objects.get(id=agent_pk)
        delete_record.delete()
        messages.success(request, "Record Deleted")
        return redirect('agent')
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

def assign_customer(request, customer_id, agent_id=None):
    if request.user.is_authenticated:
        customer = get_object_or_404(Customer, id=customer_id)
        agents = Agent.objects.all()

        if customer.agent:
            messages.error(request, f"{customer.first_name } is already assigned")
            return redirect('home')

        # Assign the agent to the customer
        if request.method == "POST":
            agent_id = request.POST.get('agent_id')
            if agent_id:
                agent = get_object_or_404(Agent, id=agent_id)
                customer.agent = agent
                customer.save()
                messages.success(request, "Customer assigned!")
                return redirect('home')
            else:
                messages.error(request, "No agent selected for assignment")
                return redirect('assign_customer', customer_id=customer.id)
        return render(request, 'assign_customer.html', {'customer': customer, 'agents': agents})
    else:
        messages.error(request, "login to assign a lead")
        return redirect('home')

def select_customer(request):
    if request.user.is_authenticated:
        customers = Customer.objects.all()
        return render(request, 'select_customer.html', {'customers':customers})
    else:
        messages.success(request, "Login to select a customer")
        return redirect('home')

def add_order(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            order_form = OrderForm(request.POST)
            if order_form.is_valid():
                order_form.save()
                messages.success(request, "Order added successfully!")
                return redirect('add_order')
            else:
                messages.error(request, "Error adding order. Please check the form")
        else:
            order_form = OrderForm()
    else:
        messages.error(request, "Please login to add orders")
        return redirect('home')

    total_delivered = Order.objects.filter(status='delivered').count()
    total_pending = Order.objects.filter(status='pending').count()
    customers_with_orders = Customer.objects.filter(order__isnull=False).distinct() 
    orders = Order.objects.select_related('customer', 'product').all()
            

    context = {
        'order_form': order_form,
        'total_delivered': total_delivered,
        'total_pending': total_pending,
        'customers_with_orders': customers_with_orders,
        'orders': orders,
    }

    return render(request, 'add_order.html', context) 

def order_delete(request, pk):
    if request.user.is_authenticated:
        order = Customer.objects.get(id=pk)
        order.delete()
        messages.success(request, "Order deleted successfully!")
        return redirect('home')
    else:
        messages.success(request, "Login to delete records..")
        return redirect('home')
