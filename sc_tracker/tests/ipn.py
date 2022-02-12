import decimal

from django.test import TestCase
from django.utils import timezone
from paypal.standard.ipn.models import PayPalIPN
from paypal.standard.models import ST_PP_COMPLETED

from ..hooks import handle_valid_ipn
from ..models import Donation, Marathon


class IPNTestCase(TestCase):
    def setUp(self):
        self.marathon = Marathon.objects.create(
            start_time=timezone.now(),
            name="TestCon2022",
            slug="tc2022",
            recipient_name="example",
            recipient_paypal="example@example.com",
            currency=Marathon.EURO,
        )

    def test_ipn_correct(self):
        donation = Donation.objects.create(
            event=self.marathon, amount=decimal.Decimal(1.0)
        )
        ipn = PayPalIPN.objects.create(
            business="example@example.com",
            receiver_email="example@example.com",
            txn_id="abc",
            payer_id="def",
            amount="1.0",
            custom=f'{donation.pk}:"onestay"',
            payment_status=ST_PP_COMPLETED,
        )

        self.assertEqual(handle_valid_ipn(ipn), True)

    def test_ipn_wrong_email(self):
        donation = Donation.objects.create(
            event=self.marathon, amount=decimal.Decimal(1.0)
        )
        ipn = PayPalIPN.objects.create(
            business="notexample@example.com",
            receiver_email="notexample@example.com",
            txn_id="abc",
            payer_id="def",
            amount="1.0",
            custom=f'{donation.pk}:"onestay"',
            payment_status=ST_PP_COMPLETED,
        )

        self.assertEqual(handle_valid_ipn(ipn), False)

    def test_ipn_wrong_custom(self):
        donation = Donation.objects.create(
            event=self.marathon, amount=decimal.Decimal(1.0)
        )
        ipn = PayPalIPN.objects.create(
            business="notexample@example.com",
            receiver_email="notexample@example.com",
            txn_id="abc",
            payer_id="def",
            amount="1.0",
            custom=f'{donation.pk}:onestay"',
            payment_status=ST_PP_COMPLETED,
        )

        Donation.objects.create(event=self.marathon, amount=decimal.Decimal(1.0))

        ipn2 = PayPalIPN.objects.create(
            business="example@example.com",
            receiver_email="example@example.com",
            txn_id="abc",
            payer_id="def",
            amount="1.0",
            custom=f'55:"onestay"',
            payment_status=ST_PP_COMPLETED,
        )

        self.assertEqual(handle_valid_ipn(ipn), False)
        self.assertEqual(handle_valid_ipn(ipn2), False)

    def test_ipn_wrong_amount(self):
        donation = Donation.objects.create(
            event=self.marathon, amount=decimal.Decimal(2.0)
        )
        ipn = PayPalIPN.objects.create(
            business="example@example.com",
            receiver_email="example@example.com",
            txn_id="abc",
            payer_id="def",
            amount="1.0",
            custom=f'{donation.pk}:"onestay"',
            payment_status=ST_PP_COMPLETED,
        )

        self.assertEqual(handle_valid_ipn(ipn), False)
