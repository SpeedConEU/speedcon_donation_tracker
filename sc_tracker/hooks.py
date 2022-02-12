import decimal
import re

from paypal.standard.ipn.models import PayPalIPN
from paypal.standard.models import ST_PP_COMPLETED

from . import logger
from .models import Donor, Donation

alias_re = re.compile('^".*"$')


# FIXME: throw an exception instead of returning a bool
def handle_valid_ipn(sender: PayPalIPN, **kwargs) -> bool:
    if sender.payment_status == ST_PP_COMPLETED:
        custom = sender.custom.split(":", maxsplit=1)
        if len(custom) != 2:
            logger.error(f"invalid IPN custom value received '{custom}'")
            return False
        try:
            donation_id = int(custom[0], 10)
        except ValueError:
            logger.error(f"donation id {custom[0]} is not a valid int")
            return False

        if alias_re.match(custom[1]) is None or len(custom[1]) < 3:
            logger.error(f'alias "{custom[1]}" is not properly formatted')
            return False

        alias = custom[1][1:-1]

        try:
            donation = Donation.objects.get(pk=donation_id)
        except Donation.DoesNotExist:
            logger.error(f"donation {donation_id} does not exist")
            return False

        recipient_email = sender.business if sender.business else sender.receiver_email
        if donation.event.recipient_paypal != recipient_email:
            logger.error(
                f"{recipient_email=} does not match {donation.event.recipient_paypal=} for {sender.txn_id=}"
            )
            return False

        if donation.amount != decimal.Decimal(sender.amount):
            logger.error(
                f"{sender.amount=} does not match {donation.amount=} for {sender.txn_id=}"
            )
            return False

        try:
            donor = Donor.objects.get(payer_id=sender.payer_id)
            # same user chose a new alias, update it
            if donor.alias.lower() != alias.lower():
                donor.alias = alias
            donor.save()
        except Donor.DoesNotExist:
            donor = Donor.objects.create(alias=alias, payer_id=sender.payer_id)

        donation.donor = donor
        donation.transaction_state = Donation.COMPLETED
        donation.txn_id = sender.txn_id
        donation.save()

        return True

    return False


def handle_invalid_ipn(ipn_obj: PayPalIPN):
    logger.log(f"Invalid paypal IPN received {ipn_obj.txn_id=}")
