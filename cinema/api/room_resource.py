from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest

from ..validations.room_validator import RoomValidator
from ..models import Room


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

