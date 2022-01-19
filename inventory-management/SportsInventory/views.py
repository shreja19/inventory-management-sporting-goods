from django.shortcuts import render
from users.forms import UserSignupForm


# Create your views here.
def index(request):
    return render(request, 'login.html', {})

def logout(request):
    return render(request, 'login.html', {})

def cust_reg(request):
    form = UserSignupForm()
    return render(request, 'registrn.html', {'form': form})


