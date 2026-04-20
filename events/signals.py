from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from events.models import Event, TicketType

@receiver(post_save, sender=Event)
@receiver(post_delete, sender=Event)
def clear_event_cache(sender, instance, **kwargs):
    cache.delete(f"event_detail_cache_{instance.uuid}")
    for page in range(1, 51):
        cache.delete(f"events_list_cache_page_{page}")


@receiver(post_save, sender=TicketType)
@receiver(post_delete, sender=TicketType)
def clear_ticket_type_cache(sender, instance, **kwargs):
    cache.delete(f"event_detail_cache_{instance.event.uuid}")
    for page in range(1, 51):
        cache.delete(f"events_list_cache_page_{page}")
