from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db import models

from .models import Event, Category, PhysicalEvent, OnlineEvent, Location

from django.utils import timezone
from django.contrib.auth.models import User

"""
class ListLocationSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        import pdb
        pdb.set_trace()
"""


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        # list_serializer_class = ListLocationSerializer
        model = Location
        fields = '__all__'


class CategoryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)


class EventListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        iterable = data.all() if isinstance(data, models.Manager) else data
        serialized_data = [OnlineEventSerializer(context=self.context).to_representation(
            instance=item._onlineevent_cache) if item._onlineevent_cache else PhysicalEventSerializer(
            context=self.context).to_representation(instance=item._physicalevent_cache)
                           for item in iterable]
        return serialized_data


class EventSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    categories = CategoryTypeSerializer(many=True, read_only=True)
    type = serializers.ChoiceField(choices=[('online', 'Online'), ('physical', 'Physical')], write_only=True)
    is_mine = serializers.SerializerMethodField(read_only=True)

    def create(self, validated_data):
        validated_data.pop('type', None)
        return super(EventSerializer, self).create(validated_data)

    def get_is_mine(self, event):
        return event.author == self.context['request'].user

    def validate_start(self, start):
        """Validates start field to ensure it is a date in the future"""

        if start < timezone.now():
            raise ValidationError("Please choose a time in the future not the past")
        return start

    def validate(self, data):
        """Validates end time and checks to see if no events clash"""

        # Check date times
        dates = [data['start'], data['end']]

        # Checks the end time does not start before the end time
        if dates[1] < dates[0]:
            raise ValidationError("End must occur after start")

        # Queries the database to find datetimes that clash with current events
        events = Event.objects.filter(end__gte=dates[0], start__lte=dates[1])
        if events:
            raise ValidationError("Time clashes with events: " + ', '.join([str(e) for e in events]) +
                                  ". Please choose an alternative time.")
        return data

    def get_author(self, event):
        user = event.author
        return "{} {}".format(user.first_name, user.last_name)

    class Meta:
        model = Event
        fields = ('id', 'start', 'end', 'label', 'author', 'categories', 'type', 'is_mine')
        list_serializer_class = EventListSerializer


class EventCategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    add_categories = serializers.PrimaryKeyRelatedField(many=True,
                                                        write_only=True,
                                                        queryset=Category.objects.all(),
                                                        allow_null=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'add_categories')


class CategorySerializer(serializers.ModelSerializer):
    add_to_all_events = serializers.BooleanField(write_only=True)
    number_of_events = serializers.IntegerField(read_only=True, source='num_events')
    next_upcoming_event = serializers.DateTimeField(read_only=True, source='upcoming_event')

    class Meta:
        model = Category
        fields = ('id', 'name', 'number_of_events',
                  'next_upcoming_event', 'add_to_all_events')
        depth = 1


class UserSerializer(serializers.ModelSerializer):
    events = serializers.SlugRelatedField(many=True,
                                          read_only=True,
                                          slug_field='label')

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'events',)
        depth = 1


class OnlineEventSerializer(EventSerializer):
    event_type = serializers.CharField(read_only=True, default="Online")
    url = serializers.URLField(default='')

    class Meta(EventSerializer.Meta):
        model = OnlineEvent
        fields = EventSerializer.Meta.fields + ('event_type', 'url',)


class PhysicalEventSerializer(EventSerializer):
    event_type = serializers.CharField(read_only=True, default="Physical")
    location = LocationSerializer(many=True, read_only=True)

    class Meta(EventSerializer.Meta):
        model = PhysicalEvent
        fields = EventSerializer.Meta.fields + ('event_type', 'location',)
        depth = 1

    def to_representation(self, instance):
        if hasattr(instance, '_physicalevent_cache'):
            instance = instance._physicalevent_cache
        return super(PhysicalEventSerializer, self).to_representation(instance)
