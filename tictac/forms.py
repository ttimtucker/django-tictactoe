from django import forms

class ButtonForm(forms.Form):
    button_name=forms.CharField(max_length=100)