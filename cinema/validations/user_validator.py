from tastypie.validation import Validation


class UserValidator(Validation):
    def is_valid(self, bundle, request=None):
        errors = {}
        
        # validate creation
        if request and request.method == 'POST':
            validation = self.validate_create(bundle)
            if validation:
                for key, value in validation:
                    errors[key] = value
        
        if errors:
            return errors

        return None
        
    def validate_create(self, bundle):
        errors = {}

        if not bundle.data.get('email'):
            errors['email'] = 'Email is required.'
            
        if not bundle.data.get('password'):
            errors['password'] = 'Password is required.'
        
        if errors:
            return errors

        return None
        