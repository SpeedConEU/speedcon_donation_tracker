from django.urls import path, include

from . import views

app_name = "sc_tracker"
urlpatterns = [
    path("", views.index, name="index"),
    path("paypal/return", views.paypal_return, name="paypal_return"),
    path("paypal/ipn", include("paypal.standard.ipn.urls")),
]
