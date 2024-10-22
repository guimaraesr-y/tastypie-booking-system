from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest
from django.contrib.auth.models import User

from cinema.validations.user_validator import UserValidator
from .models import Profile


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
