from rest_framework import mixins
from rest_framework import viewsets
import django_filters

from . import serializers
from .models import Event
from epic_crm.users.models import UserEpic


from rest_framework.permissions import IsAuthenticated
from .permissions import IsManager, IsTheAssignedSalespersonOrManager, IsTheAssignedOrManagerObject


class EventsFilter(django_filters.FilterSet):
    class Meta:
        model = Event
        fields = {
            'contract__client__name': ['exact', 'contains'],
            'contract__client__email': ['exact', 'contains'],
            'date': ['exact', 'gt', 'lt', 'gte', 'lte'],
        }


class EventsViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):

    filterset_class = EventsFilter

    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        match self.action:
            case 'create':
                permission_classes.append(IsTheAssignedSalespersonOrManager)

            case 'update':
                permission_classes.append(IsTheAssignedOrManagerObject)

            case 'destroy':
                permission_classes.append(IsManager)

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        events = Event.objects.all().order_by('date')
        return events

    def get_serializer_class(self):

        match self.action:
            case 'list':
                return serializers.EventSerializerList

            case 'retrieve':
                return serializers.EventSerializerDetails

            case 'create':
                if self.request.user.role == UserEpic.Roles.MANAGER:
                    return serializers.EventSerializerCreateByManager
                else:
                    return serializers.EventSerializerCreateBySalesPerson

            case 'update':
                if self.request.user.role == UserEpic.Roles.MANAGER:
                    return serializers.EventSerializerCreateByManager
                else:
                    return serializers.EventSerializerUpdateBySalesperson
