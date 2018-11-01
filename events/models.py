from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from icalendar import Event as Eve, vDatetime


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def add_category_to_all_events(self):
        """Adds the category to all events"""

        events = Event.objects.all()
        for event in events:
            event.categories.add(self)


class Event(models.Model):
    start = models.DateTimeField(auto_now=False)
    end = models.DateTimeField(auto_now=False)
    label = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category)
    author = models.ForeignKey('auth.User', related_name='events', on_delete=models.CASCADE)

    def __str__(self):
        return self.label + " " + str(self.id)

    def export_event(self):
        """Exports the event to ics"""

        cal = Eve()
        cal.add('summary', str(self.categories))
        cal.add('description', self.label)
        cal.add('dtstart', vDatetime(self.start))
        cal.add('dtend', vDatetime(self.end))
        return cal.to_ical()

    def is_upcoming(self):
        """Checks to see if the event is starting in the next 24 hours"""

        return timezone.now() < self.start < timezone.now() + timedelta(days=1)

    def has_happened(self):
        """Checks to see if the event has taken place"""

        return self.end < timezone.now()


class Location(models.Model):
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=50)
    postcode = models.CharField(max_length=50)

    def __str__(self):
        return self.address


class OnlineEvent(Event):
    url = models.URLField(max_length=300)


class PhysicalEvent(Event):
    location = models.ManyToManyField(Location)
