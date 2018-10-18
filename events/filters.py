import django_filters as filters
from .models import Event
from django.db.models import Q


class EventFilter(filters.FilterSet):
    first_name = filters.CharFilter(field_name='author', label='First name', method='filter_by_first_name')
    last_name = filters.CharFilter(field_name='author', label='Last name', method='filter_by_last_name')

    def filter_by_first_name(self, queryset, name, value):
        return queryset.filter(Q(author__first_name=value))

    def filter_by_last_name(self, queryset, name, value):
        return queryset.filter(author__last_name=value)

    class Meta:
        model = Event
        fields = ['categories', 'label', 'first_name', 'last_name',]
