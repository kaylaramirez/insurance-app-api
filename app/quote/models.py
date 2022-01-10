import string
import random

from django.db import models
from django.core.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _

from django.conf import settings

from django.core.validators import MinLengthValidator

from quote.constants import BASE_RATE, STATE_CODES, \
                            PREV_POLICY_CANCELLED_FEE_AMT, \
                            STATE_FEE_AMT, \
                            MILES_0_100_FEE_AMT, MILES_101_200_FEE_AMT, \
                            MILES_201_500_FEE_AMT,\
                            NO_PREV_POLICY_CANCELLED_DIS_AMT, \
                            PROPERTY_OWNER_DIS_AMT, STATES_WITH_VOLCANOES


def validate_state_code(value):
    if value not in STATE_CODES:
        raise ValidationError(_(f'Invalid state code. {value}'))


class Address(models.Model):
    """Address for a quote"""

    street_address_1 = models.CharField(max_length=255)
    street_address_2 = models.CharField(max_length=255, blank=True,
                                        null=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2, validators=[validate_state_code])
    zipcode = models.CharField(max_length=5,)

    def __str__(self):
        return f'{self.street_address_1} {self.street_address_2}, ' \
               f'{self.city}, {self.state} {self.zipcode}'


class Quote(models.Model):
    """"Quote Object"""

    @staticmethod
    def generate_quote_id():
        while True:
            q_id = ''.join(random.choices(string.ascii_uppercase +
                                          string.digits, k=10))
            if not Quote.objects.filter(quote_id=q_id).exists():
                break
        return q_id

    quote_id = models.CharField(max_length=10,
                                default=generate_quote_id.__func__,
                                validators=[MinLengthValidator(10)])
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,)
    effective_data = models.DateField(blank=True, null=True)
    previous_policy_cancelled = models.BooleanField(default=False)
    miles_to_volcano = models.IntegerField()
    property_owner = models.BooleanField(default=False)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.quote_id

    @property
    def term_premium(self):
        return BASE_RATE - self.total_discounts + self.total_fees

    @property
    def monthly_premium(self):
        # return((BASE_RATE / 6) + self.monthly_fees - self.monthly_discounts)
        return round(self.term_premium / 6, 3)

    @property
    def total_fees(self):
        return self.previous_policy_cancelled_fee + \
               self.miles_to_volcano_fee + \
               self.state_fee

    @property
    def monthly_fees(self):
        return round(self.total_fees / 6, 3)

    @property
    def total_discounts(self):
        return self.no_previous_policy_cancelled_discount + \
               self.property_owner_discount

    @property
    def monthly_discounts(self):
        return round(self.total_discounts / 6, 3)

    @property
    def previous_policy_cancelled_fee(self):
        if self.previous_policy_cancelled:
            return round(BASE_RATE * PREV_POLICY_CANCELLED_FEE_AMT, 3)
        else:
            return 0

    @property
    def miles_to_volcano_fee(self):

        if self.miles_to_volcano < 101:
            fee = MILES_0_100_FEE_AMT
        elif self.miles_to_volcano < 201:
            fee = MILES_101_200_FEE_AMT
        elif self.miles_to_volcano < 501:
            fee = MILES_201_500_FEE_AMT
        else:
            fee = 0

        return round(BASE_RATE * fee, 3)

    @property
    def state_fee(self):
        if getattr(self.address, 'state') in STATES_WITH_VOLCANOES:
            return round(BASE_RATE * STATE_FEE_AMT, 3)
        else:
            return 0

    @property
    def no_previous_policy_cancelled_discount(self):
        if not self.previous_policy_cancelled:
            return round(BASE_RATE * NO_PREV_POLICY_CANCELLED_DIS_AMT, 3)
        else:
            return 0

    @property
    def property_owner_discount(self):
        if self.property_owner:
            return round(BASE_RATE * PROPERTY_OWNER_DIS_AMT, 3)
        else:
            return 0
