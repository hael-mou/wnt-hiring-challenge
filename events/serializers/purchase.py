
from rest_framework import serializers


class PurchaseSerializer(serializers.Serializer):
    ticket_type_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1)
    customer_email = serializers.EmailField()
