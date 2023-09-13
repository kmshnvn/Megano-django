from django import forms
from .models import Delivery, OrderStatus, Order
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from phone_field import PhoneField


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "first_name",  "last_name",  "email"

    phone = forms.CharField()


class DeliveryStep2Form(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = "delivery_type", "city", "address"


class DeliveryStep3Form(forms.ModelForm):
    class Meta:
        model = Delivery
        fields ="pay",
