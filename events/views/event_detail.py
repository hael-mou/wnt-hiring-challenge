
from rest_framework import generics
from rest_framework.response import Response
from django.core.cache import cache
from events.models import Event
from events.serializers import EventDetailSerializer


class EventDetailView(generics.RetrieveAPIView):
    serializer_class =  EventDetailSerializer
    lookup_field     =  "uuid"


    def get_queryset(self):
        return (
            Event.objects
            .select_related("venue")
            .prefetch_related("tickettype_set")
        )


    def retrieve(self, request, *args, **kwargs):
        uuid = kwargs.get("uuid")
        cache_key = f"event_detail_cache_{uuid}"


        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        cache.set(cache_key, data, timeout=3600)

        return Response(data)
