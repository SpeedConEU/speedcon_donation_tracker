import decimal

from django.test import TestCase
from django.utils import timezone
from paypal.standard.ipn.models import PayPalIPN
from paypal.standard.models import ST_PP_COMPLETED

from sc_tracker.models import Marathon, Donation
from ..hooks import handle_valid_ipn


class DonationTestCase(TestCase):
    def setUp(self):
        self.marathon = Marathon.objects.create(
            start_time=timezone.now(),
            name="TestCon2022",
            slug="tc2022",
            recipient_name="VGP",
            recipient_paypal="example@example.com",
            currency=Marathon.EURO,
        )

        donation = Donation.objects.create(
            event=self.marathon, amount=decimal.Decimal(1.0)
        )

        self.ipn = PayPalIPN.objects.create(
            business="example@example.com",
            receiver_email="example@example.com",
            txn_id="abc",
            payer_id="def",
            amount="1.0",
            custom=f'{donation.pk}:"onestay"',
            payment_status=ST_PP_COMPLETED,
        )

    def test_donations_get_total(self):
        self.assertEqual(self.marathon.donations_get_total(), 0)
        handle_valid_ipn(self.ipn)
        self.assertEqual(
            Marathon.objects.get(slug__exact="tc2022").donations_get_total(), 1.0
        )
