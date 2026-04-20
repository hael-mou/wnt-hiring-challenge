
from rest_framework import serializers
from events.models import Event


class EventListSerializer(serializers.ModelSerializer):
    venue_name = serializers.CharField(source='venue.name', read_only=True)
    total_available_tickets = serializers.IntegerField(read_only=True)

    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = ["uuid", "created_at"]

