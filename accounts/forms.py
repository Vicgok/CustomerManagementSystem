from django.forms import ModelForm, fields
from .models import Order

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'