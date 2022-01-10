import logging

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from quote.models import Quote

from quote.serializers import QuoteSerializer, QuoteDetailsSerializer

logger = logging.getLogger(__name__)


class QuoteViewSet(viewsets.GenericViewSet,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin):
    """Manage quotes in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = QuoteSerializer
    queryset = Quote.objects.all()
    lookup_field = 'quote_id'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        """ Return QueryDetailSerializer """

        if self.action == 'retrieve':
            return QuoteDetailsSerializer
        else:
            return QuoteSerializer
