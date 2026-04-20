
import uuid
from django.db import models


class OrderLine(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='lines')
    ticket_type = models.ForeignKey('TicketType', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.order.uuid} - {self.ticket_type.name} x{self.quantity}"
