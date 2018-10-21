#-*- encoding=UTF-8 -*-
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.

from __future__ import unicode_literals

from django.db import models


class Player(models.Model):
    account_id = models.IntegerField()
    name = models.CharField(max_length=24)
    job = models.IntegerField()
    level = models.IntegerField()
    exp = models.IntegerField()
    ip = models.CharField(max_length=15, blank=True, null=True)
    last_play = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'player'

    def __unicode__(self):
        return self.name 


class Guild(models.Model):
    name = models.CharField(max_length=12)
    sp = models.SmallIntegerField()
    master = models.IntegerField()
    level = models.IntegerField(blank=True, null=True)
    exp = models.IntegerField(blank=True, null=True)
    skill_point = models.IntegerField()
    skill = models.TextField(blank=True, null=True)
    win = models.IntegerField()
    draw = models.IntegerField()
    loss = models.IntegerField()
    ladder_point = models.IntegerField()
    gold = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'guild'

