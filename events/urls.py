from django.conf.urls import url, include
from .views import EventCategoryViewset, EventViewSet, UserViewset, CategoryViewset, LocationViewset
from rest_framework import routers


base_router = routers.DefaultRouter()
base_router.register('events', EventViewSet, base_name='event')
base_router.register('users', UserViewset, base_name='user')
base_router.register('categories', CategoryViewset, base_name='categories')
base_router.register('locations', LocationViewset, base_name='locations')

events_router = routers.SimpleRouter()
events_router.register('categories', EventCategoryViewset, base_name='eventcategories')

urlpatterns = [
    url(r'^events/(?P<parent_pk>[\d]+)/', include(events_router.urls)),
    url(r'^', include(base_router.urls)),
]


