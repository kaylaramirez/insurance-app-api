from rest_framework import serializers

from quote.models import Address, Quote


class AddressSerializer(serializers.ModelSerializer):
    """Serializer for address object"""

    class Meta:
        model = Address
        fields = (
            'id',
            'street_address_1',
            'street_address_2',
            'city',
            'state',
            'zipcode',
        )
        read_only_fields = ('id',)


class QuoteSerializer(serializers.ModelSerializer):
    """Serializer for quote object"""

    address = AddressSerializer()

    class Meta:
        model = Quote
        fields = (
            'id',
            'quote_id',
            'effective_data',
            'previous_policy_cancelled',
            'miles_to_volcano',
            'property_owner',
            'address',
        )
        read_only_fields = ('id',)

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        address = Address.objects.create(**address_data)

        quote = Quote.objects.create(address=address, **validated_data)

        return quote
