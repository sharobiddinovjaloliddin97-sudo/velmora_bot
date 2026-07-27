from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import LoyaltySerializer
from .services import LoyaltyService


class LoyaltyViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def my_loyalty(self, request):
        loyalty = LoyaltyService.get_loyalty(request.user)

        serializer = LoyaltySerializer(loyalty)

        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def redeem_voucher(self, request):
        loyalty = LoyaltyService.redeem_voucher(request.user)

        serializer = LoyaltySerializer(loyalty)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )