from tastypie.resources import ModelResource
from tastypie.exceptions import Unauthorized, NotFound
from tastypie.http import HttpUnauthorized
from tastypie.utils import trailing_slash
from tastypie import fields
from tastypie.authentication import BasicAuthentication
from django.conf.urls import url

from ..authotizations.seat_authorization import SeatAuthorization
from ..decorators import handle_exceptions
from ..models import Seat


class SeatResource(ModelResource):
    session = fields.ForeignKey('cinema.api.session_resource.SessionResource', 'session', full=False)
    
    class Meta:
        queryset = Seat.objects.all()
        resource_name = 'seat'
        always_return_data = True
        authorization = SeatAuthorization()
        allowed_methods = ['get', 'post']
        authentication = BasicAuthentication()
    
    def is_authenticated(self, request):
        if request.method == 'GET':
            return True
        
        return super(SeatResource, self).is_authenticated(request)    
    
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/reserve%s$" % 
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('reserve_seat'), name="api_reserve_seat")
        ]
    
    @handle_exceptions
    def reserve_seat(self, request, **kwargs):
        auth_result = self._meta.authentication.is_authenticated(request)
        
        if not auth_result or isinstance(auth_result, HttpUnauthorized):
            raise Unauthorized("You are not authorized to reserve a seat.")
        
        seat_id = kwargs.get('pk')
        
        try:
            bundle = self.build_bundle(request=request)
            seat = self.obj_get(bundle=bundle, pk=seat_id)
            seat.reserve(request.user)
        except Seat.DoesNotExist:
            raise NotFound("Seat not found.")
        
        return self.create_response(
            request, 
            self.full_dehydrate(self.build_bundle(obj=seat, request=request))
        )
