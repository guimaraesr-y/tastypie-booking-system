from tastypie.api import Api
from django.conf.urls import url, include

from .api.room_resource import RoomResource
from .api.seat_resource import SeatResource
from .api.user_resource import UserResource
from .api.session_resource import SessionResource


cinema_api_v1 = Api(api_name='v1')
cinema_api_v1.register(RoomResource())
cinema_api_v1.register(SeatResource())
cinema_api_v1.register(UserResource())
cinema_api_v1.register(SessionResource())

urlpatterns = [
    url(r'^api/', include(cinema_api_v1.urls)),
]
