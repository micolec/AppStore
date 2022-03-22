from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
#from .models import Ride, Bid
		
class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'phone_number', 'hall']

"""		
class Advertise(forms.ModelForm):
    class Meta:
        model = Ride
        fields = ["ride_id", "origin", "destination", "start_time", "driver"]

class Bid(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["bid_id", "username", "ride", "bid_price"]

"""
