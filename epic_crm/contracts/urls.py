from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.SimpleRouter()
router.register(r'contracts', views.UsersViewSet, basename='contracts')
# /contracts/{contracts_pk}/


urlpatterns = [
    path('', include(router.urls)),
]
