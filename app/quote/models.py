from django.db import models

from django.conf import settings


class Address(models.Model):
    """Address for a quote"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address_1 = models.CharField(max_length=255)
    street_address_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2,)
    zipcode = models.CharField(max_length=5,)

    def __str__(self):
        return f'{self.street_address_1} {self.street_address_2}, ' \
               f'{self.city}, {self.state} {self.zipcode}'


class Quote(models.Model):
    """"Quote Object"""

    quote_id = models.CharField(max_length=10)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,)
    effective_data = models.DateField(blank=True, null=True)
    previous_policy_cancelled = models.BooleanField(default=False)
    miles_to_volcano = models.IntegerField()
    property_owner = models.BooleanField(default=False)
    property_address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.quote_id
