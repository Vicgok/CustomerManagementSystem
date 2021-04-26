from os import name, truncate
from django.db import models
from django.db.models.deletion import SET_NULL
from django.contrib.auth.models import User
from django.db.models.fields import NullBooleanField

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200,blank=True, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="default-user-image.png", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        if self.name == None:
            return "ERROR-Customer name is NULL"
        return self.name

    class Meta:
        verbose_name_plural = 'Customers'

class Tag(models.Model):
    name = models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Tags'

class Product(models.Model):
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Out door','Out door'),
        )
    name = models.CharField(max_length=200, null=True)
    price = models.CharField(max_length=200,null=True)
    category = models.CharField(max_length=200,null=True,choices=CATEGORY)
    description = models.CharField(max_length=200,null=True, blank=True)
    date_created= models.DateTimeField(auto_now_add=True,null=True)
    tags = models.ManyToManyField(Tag)
    

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Products'
    
class Order(models.Model):
    STATUS = (
        ('Pending','Pending'),
        ('Out for delivery','Out for delivery'),
        ('Delivered','Delivered'),
    )
    customer = models.ForeignKey(Customer, null=True, on_delete=SET_NULL)
    product = models.ForeignKey(Product, null=True,on_delete=SET_NULL) 
    date_created= models.DateTimeField(auto_now_add=True,null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name_plural = 'Orders'