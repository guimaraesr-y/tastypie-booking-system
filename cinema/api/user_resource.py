from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest

from ..validations.user_validator import UserValidator
from ..models import User, Profile

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        authorization = Authorization()
        always_return_data = True
        validation = UserValidator()
        excludes = ['password']
    
    def obj_create(self, bundle, **kwargs):
        raw_password = bundle.data.get('password')
        birth_date = bundle.data.get('birth_date')
        bio = bundle.data.get('bio', '')
        
        try:
            bundle = super(UserResource, self).obj_create(bundle, **kwargs)
            bundle.obj.set_password(raw_password)
            bundle.obj.save()
        except Exception as e:
            raise BadRequest(u'Error when creating user: %s' % e.__str__())
        
        Profile.objects.create(
            user=bundle.obj,
            birth_date=birth_date,
            bio=bio
        )
        
        return bundle
