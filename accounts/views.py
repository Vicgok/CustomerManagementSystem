from django.shortcuts import render,redirect
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm
# Create your views here.

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

def products(request):
    products = Product.objects.all()

    return render(request,'accounts/products.html',{
        'products':products
    })

def customers(request,pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()
    total_orders = orders.count()

    context = {
        'customer':customer,
        'orders':orders,
        'total_orders':total_orders,
    }

    return render(request,'accounts/customers.html',context)

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

def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {
        'item':order
    }

    return render(request,'accounts/delete.html',context)