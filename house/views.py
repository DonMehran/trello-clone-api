from django.shortcuts import render
from rest_framework import viewsets
from .models import HouseModel
from .serializers import HouserSerializer
from .permissions import IsHouseManagerOrNone
# Create your views here.

class HouseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsHouseManagerOrNone]
    queryset = HouseModel.objects.all()
    serializer_class = HouserSerializer

    def join(self, request, pk=None):
        pass