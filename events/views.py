from rest_framework import viewsets, status
from rest_framework.decorators import action
from .models import Event, Category
from .serializers import EventSerializer, UserSerializer, CategorySerializer, EventCategorySerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from .filters import EventFilter
from .permissions import IsOwnerOrReadOnly


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_class = EventFilter
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get_queryset(self):
        return Event.objects.select_related('author')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True)
    def download_ics(self, request, pk, *args, **kwargs):
        """
        Method to download ICS file of a chosen event
        """

        event = Event.objects.get(pk=pk)
        ics_file = event.export_event()
        response = Response(ics_file)
        response['Content-Disposition'] = 'attachment; ' \
                                          'filename=' + event.label + '.ics'
        return response


class EventCategoryViewset(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventCategorySerializer

    def list(self, request, *args, **kwargs):
        pk = request.parser_context['kwargs']['parent_pk']
        qs = self.queryset
        event = qs.get(pk=int(pk))
        categories = event.categories.all()

        page = self.paginate_queryset(categories)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Gets the pk of the event which is passed in the url
        pk = request.parser_context['kwargs']['parent_pk']
        event = Event.objects.get(pk=int(pk))

        # Gets the serializer data
        add_category = serializer.validated_data.pop('add_categories')
        delete_category = serializer.validated_data.pop('delete_categories')

        if add_category:
            event.categories.add(add_category)

        if delete_category:
            event.categories.remove(delete_category)

        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        add_to_event = serializer.validated_data.pop('add_to_all_events')
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Adds category to all events if add_to_all_events is True
        if add_to_event:
            serializer.instance.add_category_to_all_events()
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
