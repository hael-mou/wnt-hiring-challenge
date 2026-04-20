
from events.models import TicketType
from rest_framework.serializers import ModelSerializer


class TicketTypeSerializer(ModelSerializer):
    class Meta:
        model = TicketType
        fields = ['uuid', 'name', 'price', 'quantity_available']
        read_only_fields = ['uuid']
        
