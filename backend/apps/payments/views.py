from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.orders.models import Order
from .serializers import PaymentSerializer
from .services import PaymentService


class PaymentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def get_payment(self, request):
        order_id = request.query_params.get("order_id")

        order = Order.objects.get(id=order_id)

        payment = PaymentService.get_payment(order)

        serializer = PaymentSerializer(payment)

        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def update_status(self, request):
        order_id = request.data.get("order_id")
        status_value = request.data.get("status")
        transaction_id = request.data.get("transaction_id")

        order = Order.objects.get(id=order_id)

        payment = PaymentService.get_payment(order)

        payment = PaymentService.update_payment_status(
            payment,
            status=status_value,
            transaction_id=transaction_id,
        )

        serializer = PaymentSerializer(payment)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )