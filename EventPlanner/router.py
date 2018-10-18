from events.views import EventViewSet, UserViewset, CategoryViewset
from rest_framework import routers

router = routers.DefaultRouter()
router.register('events', EventViewSet, base_name='event')
router.register('users', UserViewset, base_name='user')
router.register('categories', CategoryViewset, base_name='categories')
