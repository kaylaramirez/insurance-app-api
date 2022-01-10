from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from quote.models import Quote, Address

from quote.serializers import QuoteDetailsSerializer

QUOTE_URL = reverse('quote:quote-list')

TEST_QUOTE = {
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


def detail_url(quote_id):
    """Return quote detail URL"""
    return reverse('quote:quote-detail', args=[quote_id])


def sample_address(user, **parms):
    """Create a sample address object"""
    defaults = {
        'street_address_1': '7744 Northcross Drive',
        'street_address_2': None,
        'city': 'Austin',
        'state': 'TX',
        'zipcode': '78757'}
    return Address.objects.create(**defaults)


def sample_quote(user, **parms):
    """Create a sample quote object"""
    address = sample_address(user)
    defaults = {
            'effective_data': None,
            'previous_policy_cancelled': False,
            'miles_to_volcano': 400,
            'property_owner': True,
            'address': address,
    }
    return Quote.objects.create(user=user, **defaults)


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
        '''Test creating a new quote'''

        payload = {
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

    def test_create_quote_invalid_address(self):
        """Test creating a quote with invalid address"""

        TEST_QUOTE['address'] = {}
        res = self.client.post(QUOTE_URL, TEST_QUOTE, format='json')
        self.assertRaises(TypeError)
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

    def test_view_quote_details(self):
        """Test viewing a quote"""

        quote = sample_quote(user=self.user)

        url = detail_url(quote.quote_id)
        res = self.client.get(url)

        serializer = QuoteDetailsSerializer(quote)
        self.assertEqual(res.data, serializer.data)

    def test_view_quote_details_has_prop(self):
        """Test quote_details had a prop"""
        quote = sample_quote(user=self.user)

        url = detail_url(quote.quote_id)
        res = self.client.get(url)
        self.assertIn('term_premium', res.data)
