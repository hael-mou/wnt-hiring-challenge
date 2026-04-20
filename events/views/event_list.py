
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from events.serializers import EventListSerializer
from django.core.cache import cache
from rest_framework.response import Response
from events.models import Event
from django.utils import timezone
from django.db.models import Case, When, Value, IntegerField, Sum


class EventPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 50



class EventStatus():
    LIVE        = 1
    UPCOMING    = 2
    ENDED       = 3



class EventListView(generics.ListAPIView):
    serializer_class = EventListSerializer
    pagination_class = EventPagination


    def list(self, request, *args, **kwargs):
        page_num = request.query_params.get("page", 1)
        cache_key = f"events_list_cache_page_{page_num}"
        
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        
        qs = self.get_queryset()
        page_qs = self.paginate_queryset(qs)
        serializer = self.get_serializer(page_qs, many=True)
        data = self.get_paginated_response(serializer.data).data

        timeout = self.calculate_cache_timeout(qs)
        cache.set(cache_key, data, timeout)

        return Response(data)    


    def get_queryset(self):
        now = timezone.now()

        return (
            Event.objects
            .select_related("venue")
            .prefetch_related("tickettype_set")
            .annotate(
                status_order=Case(
                    When(start_date__lte=now, end_date__gte=now, then=Value(EventStatus.LIVE)),
                    When(start_date__gt=now, then=Value(EventStatus.UPCOMING)),
                    When(end_date__lt=now, then=Value(EventStatus.ENDED)),
                    output_field=IntegerField(),
                ),
                total_available_tickets=Sum("tickettype__quantity_available")
            )
            .order_by("status_order", "start_date")
        )


    def calculate_cache_timeout(self, qs):
        next_event_date = None

        for event in qs:
            if event.status_order == EventStatus.ENDED:
                break

            candidate = (
                event.end_date if event.status_order == EventStatus.LIVE
                else event.start_date
            )

            if next_event_date is None or candidate < next_event_date:
                next_event_date = candidate

        now = timezone.now()

        return (
            max(int((next_event_date - now).total_seconds()), 1)
            if next_event_date else 3600
        )
