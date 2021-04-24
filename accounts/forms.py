from django.db.models import fields
from django.forms import ModelForm, widgets
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from django import forms


from .models import Order


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class CreateUserForm(UserCreationForm):

    password1 = forms.CharField(
        label='Password:',
        widget=forms.PasswordInput(attrs={'class':'form-control mb-2', 'type':'password', 'placeholder':'Password'}),
    )
    password2 = forms.CharField(
        label='Confirm Password:',
        widget=forms.PasswordInput(attrs={'class':'form-control mb-3', 'type':'password','placeholder':'Confirm Password'}),
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets={
            'username': forms.TextInput(attrs={'class':'form-control mb-2', 'type':'text', 'placeholder':'UserName'}),
            'email':forms.TextInput(attrs={'class':'form-control mb-2', 'type':'text','placeholder':'Email'}),
        }