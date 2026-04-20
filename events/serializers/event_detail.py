
from rest_framework import serializers
from .ticket_type import TicketTypeSerializer
from events.models import Event


class EventDetailSerializer(serializers.ModelSerializer):
    venue_name = serializers.CharField(source='venue.name', read_only=True)
    ticket_types = TicketTypeSerializer(source='tickettype_set', many=True, read_only=True)

    class Meta:
        model = Event
        fields = ['uuid', 'title', 'description', 'venue_name', 'start_date', 'end_date', 'ticket_types']
        read_only_fields = ['uuid']

