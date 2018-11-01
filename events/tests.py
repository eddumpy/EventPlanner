# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from .models import Event


class DateModelTests(TestCase):

    def test_is_upcoming_for_not_upcoming_event(self):
        """Checks is_upcoming function with events that are not upcoming"""
        time = timezone.now() + timedelta(days=10)
        future_event = Event(start=time, end=time + timedelta(hours=1), label='test event', category='tests')
        self.assertIs(future_event.is_upcoming(), False)

    def test_is_upcoming_for_upcoming_event(self):
        """Checks is_upcoming with events that are upcoming"""
        time = timezone.now() + timedelta(hours=2)
        future_event = Event(start=time, end=time + timedelta(hours=1), label='test event', category='tests')
        self.assertIs(future_event.is_upcoming(), True)


def create_event(label, category, days, hours):
    """Creates an event

    :param label: The label of the Event
    :param category: The category of the Event
    :param days: What day the event will take place from now, so value 5 will indicate event starts in 5 days time
    :param hours: How long the event will last
    :return: The Event object
    """

    start_time = timezone.now() + timedelta(days=days)
    return Event.objects.create(start=start_time,
                                end=start_time + timedelta(hours=hours),
                                label=label,
                                category=category)


class EventViewsetTests(TestCase):

    def test_view_with_no_events(self):
        response = self.client.get('/api/events/')
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "No events are available")
        self.assertQuerysetEqual(response.content_data, [])
