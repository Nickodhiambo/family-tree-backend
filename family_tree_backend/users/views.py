from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
# Create your views here.


def admin_logout(request):
    """Logs out the admin"""
    logout(request)
    return HttpResponseRedirect(reverse('trees:index'))
