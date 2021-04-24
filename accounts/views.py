from django.shortcuts import render,redirect
from django.forms import inlineformset_factory

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate,login, logout
from .models import *
from .forms import OrderForm,CreateUserForm
from .filters import OrderFilter
# Create your views here.


def register(request):
    if request.user.is_authenticated:
        return redirect('accounts:home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request,'User account created for ' + user + ', login now.' )
                return redirect('accounts:login')
            


        context = {
            'form':form
        }

        return render(request,'accounts/register.html',context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('accounts:home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request,username=username,password=password)

            if user is not None:
                login(request, user)
                return redirect('accounts:home')
            else:
                messages.error(request, 'Username Or Password is incorrect!!')

        
        context = {
            }
        return render(request,'accounts/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('accounts:login')

@login_required(login_url='accounts:login')
def home(request):
    customer = Customer.objects.all()

    orders = Order.objects.all()
    total_orders = orders.count()

    delivered = orders.filter(status='Delivered').count()
    pending  = orders.filter(status='Pending').count()
    out_for_delivery = orders.filter(status='Out for delivery').count()
    context = {
        'customer': customer,
        'orders': orders,
        'total_orders': total_orders,
        'delivered':delivered,
        'pending':pending,
        'out_for_delivery':out_for_delivery
    }

    return render(request,'accounts/dashboard.html',context)
@login_required(login_url='accounts:login')
def products(request):
    products = Product.objects.all()

    return render(request,'accounts/products.html',{
        'products':products
    })

@login_required(login_url='accounts:login')
def customers(request,pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()
    total_orders = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {
        'customer':customer,
        'orders':orders,
        'total_orders':total_orders,
        'myFilter':myFilter,
    }

    return render(request,'accounts/customers.html',context)

@login_required(login_url='accounts:login')
def createOrder(request,pk):
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('product','status'),extra=5)
    customer = Customer.objects.get(id=pk)

    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    #form = OrderForm(initial={'customer':customer })
    if request.method =='POST':
        formset = OrderFormSet(request.POST,instance=customer)
        #form = OrderForm(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('/')


    context = {
        'form':formset,
        'customer':customer
    }

    return render(request,'accounts/order_form.html',context)

@login_required(login_url='accounts:login')
def updateOrder(request,pk):
    customer = Customer.objects.get(id=pk)
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method =='POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form':form,
        'customer':customer
    }

    return render(request,'accounts/order_form.html',context)

@login_required(login_url='accounts:login')
def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {
        'item':order
    }

    return render(request,'accounts/delete.html',context)