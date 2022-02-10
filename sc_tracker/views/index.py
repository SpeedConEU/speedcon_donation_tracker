from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.


def index(request):
    return render(request, "sc_tracker/index.html", {"branding": settings.BRANDING})


def paypal_return(request):
    return HttpResponse("Welcome back!")
