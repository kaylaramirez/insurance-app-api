from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from quote.models import Quote

# from quote.serializers import QuoteSerializer

QUOTE_URL = reverse('quote:quote-list')

TEST_QUOTE = {
    'quote_id': 'ABCDE12345',
    'effective_data': None,
    'previous_policy_cancelled': False,
    'miles_to_volcano': 50,
    'property_owner': False,
    'address': {
        'street_address_1': '7744 Northcross Drive',
        'street_address_2': 'N146',
        'city': 'Austin',
        'state': 'TX',
        'zipcode': '78757'
        }
    }


class PublicQuoteApiTests(TestCase):
    """Test the publicly available tags API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving tags"""
        res = self.client.post(QUOTE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class QuoteApiTests(TestCase):
    """Test the quote api"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'testuser',
            'testpass'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_get_list_not_allowed(self):
        """Test that get listing not allowed"""
        res = self.client.get(QUOTE_URL)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_quote_successful(self):
        """Test creating a new tag"""

        payload = {
            'quote_id': 'ABCDE12345',
            'effective_data': None,
            'previous_policy_cancelled': False,
            'miles_to_volcano': 50,
            'property_owner': False,
            'address': {
                'street_address_1': '7744 Northcross Drive',
                'street_address_2': 'N146',
                'city': 'Austin',
                'state': 'TX',
                'zipcode': '78757'
            }
        }
        res = self.client.post(QUOTE_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        exists = Quote.objects.filter(
            user=self.user,
            quote_id=payload['quote_id']).exists()
        self.assertTrue(exists)

    def test_create_quote_invalid_address(self):
        """Test creating a quote with invalid address"""

        TEST_QUOTE['address'] = {}
        res = self.client.post(QUOTE_URL, TEST_QUOTE, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_quote_invalid_property_owner(self):
        """Test creating a quote with invalid property owner"""

        TEST_QUOTE['property_owner'] = None
        res = self.client.post(QUOTE_URL, TEST_QUOTE, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_quote_invalid_miles(self):
        """Test creating a quote with invalid miles"""

        TEST_QUOTE['miles_to_volcano'] = 'AA'
        res = self.client.post(QUOTE_URL, TEST_QUOTE, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
