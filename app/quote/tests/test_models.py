from django.contrib.auth import get_user_model
from django.test import TestCase

from quote import models


class ModelsTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'testpass'
        )

    def test_address_str(self):
        """Test the address string representation"""
        address = models.Address.objects.create(
            # user=self.user,
            street_address_1='7744 Northcross Drive',
            street_address_2='N146',
            city='Austin',
            state='TX',
            zipcode='78757'
        )
        str_add = '7744 Northcross Drive N146, Austin, TX 78757'
        self.assertEqual(str(address), str_add)

    def test_quote_id_generated(self):
        """Test the quote string representation"""

        address = models.Address.objects.create(
            # user=self.user,
            street_address_1='7744 Northcross Drive',
            street_address_2='N146',
            city='Austin',
            state='TX',
            zipcode='78757'
        )

        quote = models.Quote.objects.create(
            user=self.user,
            quote_id='ABCDE12345',
            effective_data=None,
            previous_policy_cancelled=False,
            miles_to_volcano=50,
            property_owner=False,
            address=address,
        )

        self.assertEqual(len(str(quote)), 10)
