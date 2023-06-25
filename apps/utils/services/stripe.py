import logging
from django.conf import settings

import stripe

logger = logging.getLogger('custom')


def get_use_stripe(amount):
    stripe_min_amount = 50
    stripe_amount = int(round(amount, 2) * 100)
    return stripe_amount > stripe_min_amount


class StripeHandler:
    """
    A module to handle Stripe API related operations.
    """

    def __init__(self, api_key=None, currency=None):
        stripe.api_key = api_key or settings.STRIPE_SECRET_KEY
        self.currency = currency or settings.STRIPE_CURRENCY

    def get_stripe_amount(self, amount):
        return int(round(amount, 2) * 100)

    def get_use_stripe(self, amount):
        return get_use_stripe(amount)

    def create_customer(self, email):
        try:
            return stripe.Customer.create(email=email)
        except stripe.error.StripeError as e:
            logger.error(f"Stripe Service: Error creating customer: {e}")

        return False

    def retrieve_customer(self, customer_id):
        return stripe.Customer.retrieve(customer_id)

    def create_payment_intent(self, customer, amount):
        try:
            return stripe.PaymentIntent.create(
                amount=self.get_stripe_amount(amount),
                currency=self.currency,
                customer=customer['id'],
                metadata={
                    'order_amount': amount
                }
            )

        except stripe.error.StripeError as e:
            logger.error(f"Stripe Service: Error creating payment intent: {e}")

        return False

    def retrieve_payment_intent(self, intent_id, client_secret=None):
        return stripe.PaymentIntent.retrieve(id=intent_id, client_secret=client_secret)

    def update_payment_intent(self, intent, **kwargs):
        return stripe.PaymentIntent.modify(intent['id'], **kwargs)
