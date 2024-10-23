from tastypie.validation import Validation


class RoomValidator(Validation):
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

        if not bundle.data.get('rows') or bundle.data.get('rows') < 1:
            errors['rows'] = 'Rows should be greater than 0.'
            
        if not bundle.data.get('columns') or bundle.data.get('columns') < 1:
            errors['columns'] = 'Columns should be greater than 0.'
        
        if errors:
            return errors

        return None
        