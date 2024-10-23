from tastypie.api import Api
from django.conf.urls import url, include, url
from django.contrib import admin

from cinema.api import RoomResource, SeatResource, SessionResource, UserResource


v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(RoomResource())
v1_api.register(SessionResource())
v1_api.register(SeatResource())

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(v1_api.urls)),
]
