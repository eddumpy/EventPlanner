from django.conf.urls import url, include
from django.contrib import admin
from .router import router
import debug_toolbar


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api/rest-auth/', include('rest_framework.urls')),
]

urlpatterns += [
    url(r'^__debug__/', include(debug_toolbar.urls)),
]
