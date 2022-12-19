from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.SimpleRouter()
router.register(r'clients', views.UsersViewSet, basename='clients')
# /clients/{user_pk}/


urlpatterns = [
    path('', include(router.urls)),
]
