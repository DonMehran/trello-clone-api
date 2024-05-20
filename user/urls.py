from rest_framework import routers
from .views import UserViewSet

# app_name = 'users'

router = routers.DefaultRouter()
router.register('users', UserViewSet)

from django.urls import path, include

urlpatterns = [
    path('accounts/', include(router.urls))
]