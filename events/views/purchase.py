
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from events.models import Event, TicketType, Order, OrderLine
from events.serializers import PurchaseSerializer


class PurchaseView(APIView):

    def post(self, request, pk):
        serializer = PurchaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            event = Event.objects.get(uuid=pk)
        except Event.DoesNotExist:
            return Response(
                {"error": "Event not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            quantity = serializer.validated_data["quantity"]
            
            with transaction.atomic():
                ticket_type = TicketType.objects.select_for_update().get(
                    uuid=serializer.validated_data["ticket_type_id"],
                    event=event
                )

                if ticket_type.quantity_available < quantity:
                    return Response(
                        {"error": "Not enough tickets available"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                ticket_type.quantity_available -= quantity
                ticket_type.save(update_fields=["quantity_available"])

                total_price = ticket_type.price * quantity

                order = Order.objects.create(
                    event=event,
                    customer_email=serializer.validated_data["customer_email"],
                    status="confirmed",
                )

                OrderLine.objects.create(
                    order=order,
                    ticket_type=ticket_type,
                    quantity=quantity,
                )

        except TicketType.DoesNotExist:
            return Response(
                {"error": "Ticket type not found for this event"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "order_id": str(order.uuid),
                "event": event.title,
                "ticket_type": ticket_type.name,
                "quantity": quantity,
                "total_price": str(total_price),
                "status": "confirmed",
            },
            status=status.HTTP_201_CREATED,
        )
