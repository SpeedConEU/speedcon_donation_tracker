from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm

from ..models import Marathon, Donation, Comment
from ..forms import DonateForm


def donate_view(request, slug):
    marathon = get_object_or_404(Marathon, slug=slug)
    if not marathon.accept_donations:
        return HttpResponseRedirect(reverse("sc_tracker:index"))

    if request.method == "POST":
        form = DonateForm(request.POST)
        if form.is_valid():
            donation = Donation.objects.create(
                event=marathon,
                amount=form.cleaned_data["amount"],
                is_anon=form.cleaned_data["is_anon"],
            )

            Comment.objects.create(id=donation, text=form.cleaned_data["comment"])

            return HttpResponseRedirect(reverse("sc_tracker:index"))
    else:
        form = DonateForm()
    return render(
        request,
        "sc_tracker/donate.html",
        {
            "branding": settings.BRANDING,
            "marathon": marathon,
            "form": form,
            "is_test": settings.PAYPAL_TEST,
        },
    )


def donate(request):
    marathon = Marathon.objects.order_by("start_time")
    if len(marathon) == 0:
        return HttpResponseRedirect(reverse("sc_tracker:index"))

    slug = marathon[0].slug
    return HttpResponseRedirect(reverse("sc_tracker:donate", args=(slug,)))


BASE_URL = "https://53db-2001-9b0-212-ac00-90fa-cc03-5c95-b100.ngrok.io"


def make_paypal_form(donation_id, alias, amount):
    form = PayPalPaymentsForm(
        button_type="donate",
        initial={
            # CMD
            "cmd": "_donations",
            # HTML variables for special PayPal features
            "notify_url": f"{BASE_URL}/paypal/ipn",
            # Individual items variables
            "amount": f"{amount}",
            "item_name": "Save The Children",
            # Payment transaction variables
            "currency_code": "EUR",
            "custom": f"{donation_id}:{alias}",
            "paymentaction": "sale",
            "business": "mariusmeschter99-facilitator@gmail.com",
            # PayPal checkout page variables
            "no_shipping": "1",
            "return": f"{BASE_URL}/paypal/return?status=success",
            "rm": "1",
            "cancel_return": f"{BASE_URL}/paypal/return?status=cancel",
        },
    )

    return form
