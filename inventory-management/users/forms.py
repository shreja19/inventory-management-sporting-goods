from django import forms
from .models import UserSignupModel


class UserSignupForm(forms.ModelForm):
    firstname = forms.CharField(widget=forms.TextInput(attrs={'pattern': '[a-zA-Z]+','id': 'user', 'class': 'input'}),
                                required=True, max_length=100)
    lastname = forms.CharField(widget=forms.TextInput(attrs={'pattern': '[a-zA-Z]+', 'id': 'user', 'class': 'input'}),
                               required=True, max_length=100)

    username = forms.CharField(widget=forms.TextInput(attrs={'pattern': '[a-zA-Z]+', 'id': 'user', 'class': 'input'}),
                               required=True, max_length=100)

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'pattern': '(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}', 'id': 'user', 'class': 'input',
                                         'title': 'Must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters'}),
        required=True, max_length=100)

    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 20, 'id': 'user', 'class': 'input'}),
                              required=True, max_length=250)
    zip = forms.CharField(widget=forms.TextInput(attrs={'id': 'user', 'class': 'input'}), required=True, max_length=100)

    email = forms.CharField(
        widget=forms.TextInput(attrs={'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$', 'id': 'user', 'class': 'input'}),
        required=True, max_length=100)

    mobile = forms.CharField(widget=forms.TextInput(attrs={'pattern': '[56789][0-9]{9}', 'id': 'user', 'class': 'input'}),
                             required=True,
                             max_length=100)

    class Meta:
        model = UserSignupModel
        fields = '__all__'
