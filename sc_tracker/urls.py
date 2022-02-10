from django.urls import path, include

from .views import donate
from .views import index

app_name = "sc_tracker"
urlpatterns = [
    path("", index.index, name="index"),
    path("paypal/return", index.paypal_return, name="paypal_return"),
    path("paypal/ipn", include("paypal.standard.ipn.urls")),
    path("donate/", donate.donate, name="donate_no_marathon"),
    path("donate/<str:slug>", donate.donate_view, name="donate"),
]
