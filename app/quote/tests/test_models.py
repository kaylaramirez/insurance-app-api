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
            # quote_id='ABCDE12345',
            effective_data=None,
            previous_policy_cancelled=False,
            miles_to_volcano=50,
            property_owner=False,
            address=address,
        )

        self.assertEqual(len(str(quote)), 10)


class QuoteModelProperties(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'testpass'
        )

        address = models.Address.objects.create(
            # user=self.user,
            street_address_1='7744 Northcross Drive',
            street_address_2='N146',
            city='Austin',
            state='CO',
            zipcode='78757'
        )

        self.quote = models.Quote.objects.create(
            user=self.user,
            # quote_id='ABCDE12345',
            effective_data=None,
            previous_policy_cancelled=False,
            miles_to_volcano=400,
            property_owner=True,
            address=address,
        )

    # discounts
    def test_prop_owner_dis_prop(self):
        """Test property owner discount property"""
        self.assertEqual(self.quote.property_owner_discount, 11.988)

    def test_no_prev_cancelled_dis_prop(self):
        """Test property no prev cancelled discount"""
        self.assertEqual(self.quote.no_previous_policy_cancelled_discount,
                         5.994)

    def test_total_discounts_prop(self):
        """Test total discounts property"""
        self.assertEqual(self.quote.total_discounts, 17.982)

    def test_monthly_discounts_prop(self):
        """Test monthly discounts property"""
        self.assertEqual(self.quote.monthly_discounts, 2.997)

    # fees
    def test_state_fee_prop(self):
        """Test state fee property"""
        self.assertEqual(self.quote.state_fee, 14.985)

    def test_miles_to_volcano_fee_prop(self):
        """Test miles to volcano fee"""
        self.assertEqual(self.quote.miles_to_volcano_fee, 20.979)

    def test_previous_policy_cancelled_fee_prop(self):
        """Test prev policy cancelled fee"""
        self.assertEqual(self.quote.previous_policy_cancelled_fee, 0)

    def test_total_fees_prop(self):
        """Test total fees property"""
        self.assertEqual(self.quote.total_fees, 35.964)

    def test_monthly_fee_prop(self):
        """Test monthly fees property"""
        self.assertEqual(self.quote.monthly_fees, 5.994)

    def test_term_premium_prop(self):
        """Test term premium property"""
        self.assertEqual(self.quote.term_premium, 77.922)

    def test_monthly_premium_prop(self):
        """Test monthly premium property"""
        self.assertEqual(self.quote.monthly_premium, 12.987)
