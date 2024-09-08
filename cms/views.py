from rest_framework.permissions import IsAuthenticated
from response import CustomJsonRender
from .models import CoinDetails
from .serializers import CoindetailSerializer
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class CoindetailViewSet(mixins.ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    renderer_classes = (CustomJsonRender,)
    queryset = CoinDetails.objects.all()
    serializer_class = CoindetailSerializer
