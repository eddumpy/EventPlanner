from rest_framework import serializers
from .models import Event, Category
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User


class EventSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    categories = serializers.SlugRelatedField(
        many=True,
        queryset=Category.objects.all(),
        slug_field='name'
     )

    class Meta:
        model = Event
        fields = ('id', 'start', 'end', 'label', 'categories', 'author')
        depth = 1

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
            raise ValidationError("Time clashes with events: " + ', '.join(str(e) for e in events) +
                                  ". Please choose an alternative time.")
        return data

    def get_author(self, event):
        user = event.author
        return "{} {}".format(user.first_name, user.last_name)


class EventCategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    delete_categories = serializers.PrimaryKeyRelatedField(write_only=True,
                                                           queryset=Category.objects.all(),
                                                           allow_null=True)
    add_categories = serializers.PrimaryKeyRelatedField(write_only=True,
                                                        queryset=Category.objects.all(),
                                                        allow_null=True)

    class Meta:
        model = Category
        fields = ('id', 'name',  'add_categories', 'delete_categories',)


class CategorySerializer(serializers.ModelSerializer):
    add_to_all_events = serializers.BooleanField(write_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'add_to_all_events')


class UserSerializer(serializers.ModelSerializer):
    events = serializers.PrimaryKeyRelatedField(many=True, queryset=Event.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'events',)

