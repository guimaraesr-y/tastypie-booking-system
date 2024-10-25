from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized

class SeatAuthorization(Authorization):
    def create_detail(self, object_list, bundle):
        # Forbid seat creation
        raise Unauthorized("You are not authorized to create a seat.")

    def update_detail(self, object_list, bundle):
        # Forbid seat updates
        raise Unauthorized("You are not authorized to update a seat.")

    def delete_detail(self, object_list, bundle):
        # Forbid seat deletion
        raise Unauthorized("You are not authorized to delete a seat.")

    def read_list(self, object_list, bundle):
        # Allow anyone to read the seat list (GET request)
        return object_list

    def read_detail(self, object_list, bundle):
        # Allow anyone to read a specific seat
        return True
