from bootstrap_datepicker_plus import  DatePickerInput
from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm
)

from .models import Weightapp

class RecordingForm(forms.Form):
    choices = (
            ('Leg', 'Leg'),
            ('Shoulder', 'Shoulder'),
            ('Back', 'Back'),
            ('Arm', 'Arm'),
            ('Chest', 'Chest'),
            ('No workouts', 'No workouts')
    )
    use_date = forms.DateField(widget=DatePickerInput(format='%Y/%m/%d'))
    #use_date = forms.DateTimeField(label='Date')
    weight = forms.IntegerField(label='Weight')
    bodyfat = forms.IntegerField(label='Body fat')
    detail = forms.CharField(max_length=2000, label='Detail')
    category = forms.ChoiceField(choices=choices, label='Category')

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
