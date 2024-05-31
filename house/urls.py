from rest_framework import routers
from .views import HouseViewSet

router = routers.DefaultRouter()
router.register('houses', HouseViewSet)
