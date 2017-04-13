from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 100)
    passwd = forms.CharField(widget = forms.PasswordInput())
    btn = forms.CharField()
