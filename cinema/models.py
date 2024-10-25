# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth import get_user_model

from tastypie.exceptions import Unauthorized

from .utils import number_to_char

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)


class Room(models.Model):
    name = models.CharField(max_length=10)
    rows = models.IntegerField()
    columns = models.IntegerField()
    
    @property
    def total_seats(self):
        return self.rows * self.columns
    
    def __str__(self):
        return self.name


class Session(models.Model):
    room = models.ForeignKey(Room, related_name='sessions', on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return '%s %s-%s' % (self.room, self.start_time, self.end_time)
    
    def save(self, *args, **kwargs):
        if not self.start_time or not self.end_time:
            raise ValueError('Start and end time must be provided')
        
        if self.start_time >= self.end_time:
            raise ValueError('Start time must be before end time')
        
        super(Session, self).save(*args, **kwargs)
        self.create_seats()
    
    def create_seats(self):
        for row in range(1, self.room.rows+1):
            for column in range(1, self.room.columns+1):
                Seat.objects.create(
                    row=row,
                    column=column,
                    room=self.room,
                    session=self
                )


class Seat(models.Model):
    row = models.IntegerField()
    column = models.IntegerField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    reserved_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_reserved = models.BooleanField(default=False)
    
    @property
    def seat_id(self):
        return '%s%s' % (number_to_char(self.row), self.column)
    
    def __str__(self):
        return self.seat_id
    
    def reserve(self, user):
        if self.is_reserved:
            raise Unauthorized('Seat is already reserved')
        
        if Seat.objects.filter(session=self.session, is_reserved=True).count() >= self.room.total_seats:
            raise ValueError('Room is full')
    
        self.reserved_by = user
        self.is_reserved = True
        self.save()