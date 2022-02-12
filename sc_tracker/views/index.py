from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from ..models import Marathon


def index(request):
    marathon = Marathon.get_latest_marathon()
    return render(
        request,
        "sc_tracker/index.html",
        {"branding": settings.BRANDING, "marathon": marathon},
    )


def paypal_return(request):
    return HttpResponse("Welcome back!")
