import datetime

import pytz
from django.test import TestCase
from django.utils import timezone

from sc_tracker.models import Marathon, Donation, Donor


class MarathonTestCase(TestCase):
    def setUp(self):
        Marathon.objects.create(
            start_time=timezone.now(),
            name="TestCon2022",
            slug="tc2022",
            recipient_name="VGP",
            recipient_paypal="vgp@donation.com",
            currency=Marathon.EURO,
        )

        Marathon.objects.create(
            start_time=datetime.datetime(2021, 3, 24, 14, tzinfo=pytz.UTC),
            name="TestCon2021",
            slug="tc2021",
            recipient_name="VGP",
            recipient_paypal="vgp@donation.com",
            currency=Marathon.USD,
        )

    def test_get_latest_marathon(self):
        self.assertEqual(Marathon.get_latest_marathon().slug, "tc2022")
