from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest, NotFound
from tastypie.utils import trailing_slash
from tastypie import fields
from django.conf.urls import url

from .seat_resource import SeatResource
from .room_resource import RoomResource
from ..decorators import handle_exceptions
from ..models import Room, Seat, Session


class SessionResource(ModelResource):
    room = fields.ForeignKey('cinema.api.room_resource.RoomResource', 'room', full=False)
    
    class Meta:
        queryset = Session.objects.all()
        resource_name = 'session'
        always_return_data = True
        authorization = Authorization()
    
    def obj_create(self, bundle, **kwargs):
        try:
            bundle = super(SessionResource, self).obj_create(bundle, **kwargs)
        except Exception as e:
            raise BadRequest(u'Error when creating session: %s' % e.__str__())
        
        return bundle
    
    def prepend_urls(self):
        room_resource = RoomResource()
        room_resource_name = room_resource._meta.resource_name
        
        return [
            # find sessions by room
            url(r"^(?P<resource_name>%s)/%s/(?P<room_id>[\d]+)%s$" % 
                (self._meta.resource_name, room_resource_name, trailing_slash()),
                self.wrap_view('find_sessions_by_room'), name="api_find_sessions_by_room"),
            
            # find seats by session
            url(r"^(?P<resource_name>%s)/(?P<session_id>[\d]+)/seats%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('find_seats_by_session'), name="api_find_seats_by_session"),
        ]
        
    @handle_exceptions
    def find_sessions_by_room(self, request, **kwargs):
        room_id = kwargs.get('room_id')

        if not room_id.isdigit():
            raise BadRequest("Invalid room_id provided. It must be a number.")
        
        try:
            room = Room.objects.get(pk=room_id)
        except Room.DoesNotExist:
            raise NotFound("Room not found.")

        sessions = Session.objects.filter(room=room)
        serialized_sessions = [self.full_dehydrate(self.build_bundle(obj=session, request=request)) for session in sessions]

        return self.create_response(request, serialized_sessions)
    
    @handle_exceptions
    def find_seats_by_session(self, request, **kwargs):
        session_id = kwargs.get('session_id')

        if type(session_id) is not int and not session_id.isdigit():
            raise BadRequest("Invalid session_id provided. It must be a number.")
        
        try:
            session = Session.objects.get(pk=session_id)
        except Session.DoesNotExist:
            raise NotFound("Session not found.")

        seats = Seat.objects.filter(session=session)
        serialized_seats = [SeatResource().full_dehydrate(self.build_bundle(obj=seat, request=request)) for seat in seats]

        return self.create_response(request, serialized_seats)