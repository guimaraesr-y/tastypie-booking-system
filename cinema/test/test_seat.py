from django.test import TestCase
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse
from tastypie.test import ResourceTestCaseMixin

from cinema.models import Room, Session


class SeatResourceTest(ResourceTestCaseMixin, TestCase):
    def setUp(self):
        super(SeatResourceTest, self).setUp()
        self.api_url = reverse('api_dispatch_list', kwargs={'resource_name': 'seat', 'api_name': 'v1'})
        self.room = Room.objects.create(**{
            "name": "Room 1",
            "rows": 20,
            "columns": 10
        })
        self.session = Session.objects.create(**{
            "room": self.room,
            "start_time": "10:00",
            "end_time": "11:00"
        })
        
        self.user_username = 'johndoe'
        self.user_password = 'password'
        
        self.user = User.objects.create_user(username=self.user_username, email='johndoe@example.com')
        self.user.set_password(self.user_password)
        self.user.save()

    def get_credentials(self):
        return self.create_basic(username=self.user_username, password=self.user_password)

    def test_find_seat(self):
        url = reverse('api_dispatch_detail', kwargs={
            'resource_name': 'seat',
            'api_name': 'v1',           
            'pk': 1,
        })
        response = self.api_client.get(url, format='json')
        data = self.deserialize(response)
        
        self.assertEqual(data['row'], 1)
        self.assertEqual(data['column'], 1)
        self.assertEqual(data['is_reserved'], False)
        self.assertHttpOK(response)

    def test_create_seat(self):
        room_url = reverse('api_dispatch_detail', kwargs={'resource_name': 'room', 'api_name': 'v1', 'pk': self.room.id})
        seat_data = {
            "row": 1,
            "column": 1,
            "room": room_url,
            "session": self.session.id
        }

        response = self.api_client.post(self.api_url, data=seat_data)
        self.assertHttpUnauthorized(response)
    
    def test_update_seat(self):
        url = reverse('api_dispatch_detail', kwargs={
            'resource_name': 'seat',
            'api_name': 'v1',           
            'pk': 1,
        })
        seat_data = {
            "row": 1,
            "column": 1,
            "is_reserved": True
        }

        response = self.api_client.patch(url, data=seat_data)
        self.assertHttpMethodNotAllowed(response)
    
    def test_delete_seat(self):
        url = reverse('api_dispatch_detail', kwargs={
            'resource_name': 'seat',
            'api_name': 'v1',           
            'pk': 1,
        })
        response = self.api_client.delete(url)
        self.assertHttpMethodNotAllowed(response)
    
    def test_reserve_seat(self):
        url = reverse('api_reserve_seat', kwargs={
            'resource_name': 'seat',
            'api_name': 'v1',           
            'pk': 1,
        })

        response = self.api_client.post(url, authentication=self.get_credentials())
        self.assertHttpOK(response)
    
    def test_reserve_seat_unlogged(self):
        url = reverse('api_reserve_seat', kwargs={
            'resource_name': 'seat',
            'api_name': 'v1',           
            'pk': 1,
        })

        response = self.api_client.post(url)
        self.assertHttpUnauthorized(response)