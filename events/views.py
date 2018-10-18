from rest_framework import viewsets
from rest_framework.decorators import action
from .models import Event, Category
from .serializers import EventSerializer, UserSerializer, CategorySerializer
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

    @action(detail=True, methods=['GET', 'POST', 'DELETE'])
    def edit_categories(self, request, pk, *args, **kwargs):
        if request.method == "GET":
            qs = Event.objects.get(pk=pk)
            serializer = EventSerializer(qs)
            return Response(serializer.data)

    @action(detail=True)
    def download_ics(self, request, pk, *args, **kwargs):
        """Function to download ICS file of a chosen event"""
        event = Event.objects.get(pk=pk)
        ics_file = event.export_event()
        response = Response(ics_file)
        response['Content-Disposition'] = 'attachment; ' \
                                          'filename=' + event.label + '.ics'
        return response


class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer



