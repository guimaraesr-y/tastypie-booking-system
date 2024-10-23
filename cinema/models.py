# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from .utils import number_to_char


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
    
    def create_seats(self, session):
        for row in range(1, self.rows+1):
            for column in range(1, self.columns+1):
                Seat.objects.create(
                    row=row,
                    column=column,
                    room=self,
                    session=session
                )
    
    def __str__(self):
        return self.name


class Session(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return '%s %s-%s' % (self.room, self.start_time, self.end_time)


class Seat(models.Model):
    row = models.IntegerField()
    column = models.IntegerField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    # reserved_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_reserved = models.BooleanField(default=False)
    
    @property
    def seat_id(self):
        return '%s%s' % (number_to_char(self.row), self.column)
    
    def __str__(self):
        return self.seat_id