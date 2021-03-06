import debug_toolbar
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin/statuscheck/', include('celerybeat_status.urls')),
    url(r'^api/', include('events.urls')),
    url(r'^api/rest-auth/', include('rest_framework.urls')),
]

urlpatterns += [
    url(r'^__debug__/', include(debug_toolbar.urls)),
]
