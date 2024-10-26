from tastypie.api import Api

from cinema.urls import register_api as register_cinema

v1_api = Api(api_name='v1')

register_cinema(v1_api)