from tastypie.exceptions import BadRequest, NotFound, Unauthorized
import tastypie.http as http


def handle_exceptions(view_func):
    def _wrapped_view(self, request, *args, **kwargs):
        try:
            return view_func(self, request, *args, **kwargs)
        except (BadRequest, NotFound, Unauthorized) as e:
            return self.create_response(
                request, {'error': str(e)}, 
                response_class={
                    BadRequest: http.HttpBadRequest,
                    NotFound: http.HttpNotFound,
                    Unauthorized: http.HttpUnauthorized
                }[e.__class__]
            )
        except Exception as e:
            return self.create_response(
                request, 
                {'error': 'An unexpected error occurred: %s' % str(e)}, 
                response_class=http.HttpApplicationError
            )
    return _wrapped_view