from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Event, Category
from .serializers import EventSerializer, UserSerializer, CategorySerializer, EventCategorySerializer
from .filters import EventFilter
from .permissions import IsOwnerOrReadOnly

from django.contrib.auth.models import User
from django.db.models import Count, Min, Prefetch
from django.db.models import Q
from django.utils import timezone


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    filter_class = EventFilter
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=serializer.context['request'].user)

    def get_queryset(self):
        return Event.objects.select_related('author') \
            .prefetch_related(Prefetch('categories',
                                       queryset=Category.objects.filter(category_type__exact='P'),
                                       to_attr='physical_categories'),
                              Prefetch('categories',
                                       queryset=Category.objects.filter(category_type__exact='O'),
                                       to_attr='online_categories'))

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
    serializer_class = EventCategorySerializer

    def get_queryset(self):
        pk = self.request.parser_context['kwargs']['parent_pk']
        event = Event.objects.get(pk=int(pk))
        return event.categories

    def perform_destroy(self, instance):
        qs = self.get_queryset()
        qs.remove(instance)

    def perform_create(self, serializer):
        category_ids = [category.id for category in serializer.validated_data['add_categories']]
        qs = self.get_queryset()
        for pk in category_ids:
            category = Category.objects.get(pk=pk)
            qs.add(category)


class CategoryViewset(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def perform_create(self, serializer):
        # Removes add to event from validated data
        add_to_event = serializer.validated_data.pop('add_to_all_events')
        serializer.save()

        # If add_to_all_events is True, add to all categories
        if add_to_event:
            serializer.instance.add_category_to_all_events()

    def get_queryset(self):
        return Category.objects.annotate(num_events=Count('event'),
                                         upcoming_event=Min('event__start',
                                                            filter=Q(event__start__gt=timezone.now())))


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
