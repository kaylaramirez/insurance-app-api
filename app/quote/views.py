from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from quote.models import Quote

from quote.serializers import QuoteSerializer


class QuoteViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """Manage quotes in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = QuoteSerializer
    queryset = Quote.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
