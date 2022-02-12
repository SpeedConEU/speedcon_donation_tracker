from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm

from ..forms import DonateForm
from ..models import Marathon, Donation, Comment


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
            paypal_form = make_paypal_form(
                donation.pk,
                form.cleaned_data["alias"],
                donation.amount,
                marathon.recipient_name,
                marathon.recipient_paypal,
            )
            return render(
                request, "sc_tracker/paypal_redirect.html", {"form": paypal_form}
            )
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
    marathon = Marathon.get_latest_marathon()
    if marathon is None:
        return HttpResponseRedirect(reverse("sc_tracker:index"))

    slug = marathon.slug
    return HttpResponseRedirect(reverse("sc_tracker:donate", args=(slug,)))


def make_paypal_form(donation_id, alias, amount, recipient, recipient_mail):
    form = PayPalPaymentsForm(
        button_type="donate",
        initial={
            # CMD
            "cmd": "_donations",
            # HTML variables for special PayPal features
            "notify_url": f"https://{settings.DOMAIN}/paypal/ipn",
            # Individual items variables
            "amount": f"{amount}",
            "item_name": recipient,
            # Payment transaction variables
            "currency_code": "EUR",
            "custom": f'{donation_id}:"{alias}"',
            "paymentaction": "sale",
            "business": recipient_mail,
            # PayPal checkout page variables
            "no_shipping": "1",
            "return": f"https://{settings.DOMAIN}/paypal/return?status=success",
            "rm": "1",
            "cancel_return": f"https://{settings.DOMAIN}/paypal/return?status=cancel",
        },
    )

    return form
