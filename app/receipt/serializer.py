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
        fields = ['id', 'date_received', 'store', 'total']
        read_only_fields = ['id']


class ReceiptDetailSerializers(ReceiptSerializers):
    """
    Serializer for receipt detail view
    Receipt detail contains receipt image link
    """

    class Meta(ReceiptSerializers.Meta):
        fields = ReceiptSerializers.Meta.fields
