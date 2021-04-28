from django.db.models.fields import EmailField
from accounts.decorators import unauthenticated_user
from django.shortcuts import render,redirect
from django.forms import inlineformset_factory

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from django.contrib.auth import authenticate,login, logout
from .models import *
from .forms import OrderForm,CreateUserForm,CustomerForm
from .filters import OrderFilter

from .decorators import admin_only, unauthenticated_user, allowed_users
# Create your views here.

@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(
                user=user,
                name = user.username,
                email = email,
            )

            messages.success(request,'User account created for ' + username + ', login now.' )
            return redirect('accounts:login')
        
    context = {
        'form':form
    }

    return render(request,'accounts/register.html',context)


@unauthenticated_user
def loginPage(request):
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

# home dashboard page
@login_required(login_url='accounts:login')
@admin_only
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

# Customer user page
@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending  = orders.filter(status='Pending').count()
    out_for_delivery = orders.filter(status='Out for delivery').count()


    context = {
        'orders':orders,
        'total_orders': total_orders,
        'delivered':delivered,
        'pending':pending,
        'out_for_delivery':out_for_delivery,
    }
    return render (request,'accounts/user_page.html',context)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer

    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST,request.FILES, instance=customer)


        if form.is_valid():
            form.save()

            userUpdateField = {
                'username':customer.name,
                'email':customer.email
            }

            User.objects.filter(pk=request.user.id).update(username=userUpdateField['username'],email=userUpdateField['email'])

    context={
        'form':form
    }

    return render(request,'accounts/user_settings.html',context)







@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()

    return render(request,'accounts/products.html',{
        'products':products
    })


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
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
@allowed_users(allowed_roles=['admin'])
def createOrder(request,pk):
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('product','status'),extra=5)
    customer = Customer.objects.get(id=pk)

    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    if request.method =='POST':
        formset = OrderFormSet(request.POST,instance=customer)
        
        if formset.is_valid():
            formset.save()
            return redirect('/')


    context = {
        'form':formset,
        'customer':customer
    }

    return render(request,'accounts/order_form.html',context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
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
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {
        'item':order
    }

    return render(request,'accounts/delete.html',context)