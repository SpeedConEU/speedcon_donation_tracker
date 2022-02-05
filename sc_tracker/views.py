from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from paypal.standard.forms import PayPalPaymentsForm

BASE_URL = ''


def index(request):
    form = PayPalPaymentsForm(button_type='donate', initial={
        # CMD
        'cmd': '_donations',
        # HTML variables for special PayPal features
        'notify_url': f'{BASE_URL}/paypal/ipn',
        # Individual items variables
        'amount': '10.00',
        'item_name': 'Save The Children',
        # Payment transaction variables
        'currency_code': 'EUR',
        'custom': 'donation_id',
        'paymentaction': 'sale',
        'business': 'mariusmeschter99-facilitator@gmail.com',
        # PayPal checkout page variables
        'no_shipping': '1',
        'return': f'{BASE_URL}/paypal/return?status=success',
        'rm': '1',
        'cancel_return': f'{BASE_URL}/paypal/return?status=cancel',
    })
    return render(request, 'sc_tracker/index.html', {'form': form})


def paypal_return(request):
    return HttpResponse('Welcome back!')

