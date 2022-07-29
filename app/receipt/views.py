"""
Views for receipts APIs
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Receipt
from receipt import serializer


class ReceiptViewSet(viewsets.ModelViewSet):
    """
    Views for receipt APIs
    """
    serializer_class = serializer.ReceiptSerializers
    queryset = Receipt.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')