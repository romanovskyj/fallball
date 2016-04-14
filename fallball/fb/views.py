from rest_framework import viewsets

from .models import Reseller
from .serializers import ResellerSerializer


class ResellerViewSet(viewsets.ModelViewSet):
    queryset = Reseller.objects.all().order_by('-id')
    serializer_class = ResellerSerializer
