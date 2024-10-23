from django.test import TestCase

from django.core.urlresolvers import reverse
from tastypie.test import ResourceTestCaseMixin

from cinema.models import Room, Session


class RoomResourceTest(ResourceTestCaseMixin, TestCase):
    def setUp(self):
        super(RoomResourceTest, self).setUp()
        self.api_url = reverse('api_dispatch_list', kwargs={'resource_name': 'room', 'api_name': 'v1'})
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

    def test_create_rooms(self):
        room_data = {
            "name": "Room 1",
            "rows": 20,
            "columns": 10
        }

        response = self.api_client.post(self.api_url, data=room_data)
        self.assertHttpCreated(response)
        
    def test_invalid_room_creation(self):
        invalid_room_data = {
            "name": "Room 1",
            "rows": 20,
            "columns": 0
        }

        response = self.api_client.post(self.api_url, data=invalid_room_data)
        self.assertHttpBadRequest(response)
    
    def test_get_rooms(self):
        response = self.api_client.get(self.api_url)
        self.assertHttpOK(response)
    
    def test_get_one_room(self):
        url = reverse('api_dispatch_detail', kwargs={
            'resource_name': 'room',
            'api_name': 'v1',
            'pk': self.room.id
        })
        response = self.api_client.get(url)
        self.assertHttpOK(response)
        
    def test_get_one_room_not_found(self):
        url = reverse('api_dispatch_detail', kwargs={
            'resource_name': 'room',
            'api_name': 'v1',
            'pk': 999
        })
        response = self.api_client.get(url)
        self.assertHttpNotFound(response)
        
    def test_get_sessions(self):
        url = reverse('api_find_sessions_by_room', kwargs={
            'api_name': 'v1',           
            'room_id': self.room.id,    
            'resource_name': 'session'
        })
        response = self.api_client.get(url, format='json')
        data = self.deserialize(response)
        
        self.assertEqual(len(data), 1)
        self.assertHttpOK(response)
    
    def test_get_sessions_not_found(self):
        url = reverse('api_find_sessions_by_room', kwargs={
            'api_name': 'v1',           
            'room_id': 999,    
            'resource_name': 'session'
        })
        response = self.api_client.get(url, format='json')
        self.assertHttpNotFound(response)
