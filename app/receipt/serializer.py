"""
Serializers for receipt APIs
"""

from rest_framework import serializers

from core.models import Receipt

class ReceiptSerializers(serializers.ModelSerializer):
    """
    Serializers fro receipt objects
    """

    class Meta:
        model = Receipt
        fields = '__all__'
        read_only_fields = ['id']