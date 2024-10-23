from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest, NotFound
from tastypie.utils import trailing_slash
from django.contrib.auth.models import User
from django.conf.urls import url
from tastypie import fields

from .decorators import handle_exceptions
from .validations.user_validator import UserValidator
from .validations.room_validator import RoomValidator
from .models import Profile, Room, Seat, Session


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        authorization = Authorization()
        always_return_data = True
        validation = UserValidator()
    
    def obj_create(self, bundle, **kwargs):
        birth_date = bundle.data.get('birth_date')
        bio = bundle.data.get('bio', '')
        
        try:
            bundle = super(UserResource, self).obj_create(bundle, **kwargs)
        except Exception as e:
            raise BadRequest(u'Error when creating user: %s' % e.__str__())
        
        Profile.objects.create(
            user=bundle.obj,
            birth_date=birth_date,
            bio=bio
        )
        
        return bundle


class RoomResource(ModelResource):
    class Meta:
        queryset = Room.objects.all()
        resource_name = 'room'
        always_return_data = True
        authorization = Authorization()
        validation = RoomValidator()
    
    def obj_create(self, bundle, **kwargs):
        try:
            bundle = super(RoomResource, self).obj_create(bundle, **kwargs)
        except Exception as e:
            raise BadRequest(u'Error when creating room: %s' % e.__str__())
        
        return bundle


class SessionResource(ModelResource):
    room = fields.ForeignKey(RoomResource, 'room', full=False)
    
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
    

class SeatResource(ModelResource):
    session = fields.ForeignKey(SessionResource, 'session', full=False)
    
    class Meta:
        queryset = Seat.objects.all()
        resource_name = 'seat'
        always_return_data = True
        authorization = Authorization()
    
    def obj_create(self, bundle, **kwargs):
        try:
            bundle = super(SeatResource, self).obj_create(bundle, **kwargs)
        except Exception as e:
            raise BadRequest(u'Error when creating seat: %s' % e.__str__())
        
        return bundle