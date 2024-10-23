from django.test import TestCase

from django.core.urlresolvers import reverse
from tastypie.test import ResourceTestCaseMixin

from cinema.models import Room, Session


class SessionResourceTest(ResourceTestCaseMixin, TestCase):
    def setUp(self):
        super(SessionResourceTest, self).setUp()
        self.api_url = reverse('api_dispatch_list', kwargs={'resource_name': 'session', 'api_name': 'v1'})
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

    def test_create_session(self):
        room_url = reverse('api_dispatch_detail', kwargs={'resource_name': 'room', 'api_name': 'v1', 'pk': self.room.id})
        session_data = {
            "room": room_url,
            "start_time": "10:00",
            "end_time": "11:00"
        }

        response = self.api_client.post(self.api_url, data=session_data)
        self.assertHttpCreated(response)
        
    def test_invalid_session_creation(self):
        room_url = reverse('api_dispatch_detail', kwargs={'resource_name': 'room', 'api_name': 'v1', 'pk': self.room.id})
        invalid_session_data = {
            "room": room_url,
            "start_time": "10:00",
            "end_time": "10:00"
        }

        response = self.api_client.post(self.api_url, data=invalid_session_data)
        self.assertHttpBadRequest(response)
    
    def test_get_one_session(self):
        url = reverse('api_dispatch_detail', kwargs={
            'resource_name': 'session',
            'api_name': 'v1',
            'pk': self.session.id
        })
        response = self.api_client.get(url)
        self.assertHttpOK(response)
    
    def test_get_sessions(self):
        url = reverse('api_find_sessions_by_room', kwargs={
            'api_name': 'v1',           
            'room_id': self.room.id,    
            'resource_name': 'session'
        })
        response = self.api_client.get(url, format='json')
        data = self.deserialize(response)
        
        self.assertGreater(len(data), 0)
        self.assertHttpOK(response)
    
    def test_get_sessions_not_found(self):
        url = reverse('api_find_sessions_by_room', kwargs={
            'api_name': 'v1',           
            'room_id': 999,    
            'resource_name': 'session'
        })
        response = self.api_client.get(url, format='json')
        self.assertHttpNotFound(response)
    
    def test_get_seats(self):
        url = reverse('api_find_seats_by_session', kwargs={
            'api_name': 'v1',           
            'session_id': self.session.id,    
            'resource_name': 'session'
        })
        response = self.api_client.get(url, format='json')
        data = self.deserialize(response)
        
        self.assertEqual(len(data), self.room.rows * self.room.columns)
        self.assertHttpOK(response)
    
    def test_get_seats_not_found(self):
        url = reverse('api_find_seats_by_session', kwargs={
            'api_name': 'v1',           
            'session_id': 999,    
            'resource_name': 'session'
        })
        response = self.api_client.get(url, format='json')
        self.assertHttpNotFound(response)