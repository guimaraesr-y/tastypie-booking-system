from tastypie.exceptions import BadRequest, NotFound
import tastypie.http as http


def handle_exceptions(view_func):
    def _wrapped_view(self, request, *args, **kwargs):
        try:
            return view_func(self, request, *args, **kwargs)
        except (BadRequest, NotFound) as e:
            return self.create_response(request, {'error': str(e)}, response_class=http.HttpBadRequest if isinstance(e, BadRequest) else http.HttpNotFound)
        except Exception as e:
            return self.create_response(request, {'error': 'An unexpected error occurred: %s' % str(e)}, response_class=http.HttpInternalServerError)
    return _wrapped_view