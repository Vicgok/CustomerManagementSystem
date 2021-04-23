from accounts.models import Customer, Order, Product, Tag
from django.contrib import admin

# Register your models here.
admin.site.register(Customer)
admin.site.register(Tag)
admin.site.register(Product)
admin.site.register(Order)