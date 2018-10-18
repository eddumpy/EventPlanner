from django.conf.urls import url, include


urlpatterns = [
    url(r'^api/rest-auth/', include('rest_framework.urls')),
]