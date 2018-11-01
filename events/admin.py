from django.contrib import admin

from .models import Event, Category, OnlineEvent, PhysicalEvent, Location

admin.site.register(Event)
admin.site.register(OnlineEvent)
admin.site.register(PhysicalEvent)
admin.site.register(Category)
admin.site.register(Location)
