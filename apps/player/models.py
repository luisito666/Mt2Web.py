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


class Item(models.Model):
    owner_id = models.IntegerField()
    window = models.CharField(max_length=21)
    pos = models.SmallIntegerField()
    count = models.IntegerField()
    vnum = models.IntegerField()
    socket0 = models.CharField(max_length=100)
    socket1 = models.CharField(max_length=100)
    socket2 = models.CharField(max_length=100)
    socket3 = models.IntegerField()
    socket4 = models.IntegerField()
    socket5 = models.IntegerField()
    attrtype0 = models.IntegerField()
    attrvalue0 = models.SmallIntegerField()
    attrtype1 = models.IntegerField()
    attrvalue1 = models.SmallIntegerField()
    attrtype2 = models.IntegerField()
    attrvalue2 = models.SmallIntegerField()
    attrtype3 = models.IntegerField()
    attrvalue3 = models.SmallIntegerField()
    attrtype4 = models.IntegerField()
    attrvalue4 = models.SmallIntegerField()
    attrtype5 = models.IntegerField()
    attrvalue5 = models.SmallIntegerField()
    attrtype6 = models.IntegerField()
    attrvalue6 = models.SmallIntegerField()
    applytype0 = models.IntegerField()
    applyvalue0 = models.SmallIntegerField()
    applytype1 = models.IntegerField()
    applyvalue1 = models.SmallIntegerField()
    applytype2 = models.IntegerField()
    applyvalue2 = models.SmallIntegerField()
    applytype3 = models.IntegerField()
    applyvalue3 = models.IntegerField()
    applytype4 = models.IntegerField()
    applyvalue4 = models.IntegerField()
    applytype5 = models.IntegerField()
    applyvalue5 = models.IntegerField()
    applytype6 = models.IntegerField()
    applyvalue6 = models.IntegerField()
    applytype7 = models.IntegerField()
    applyvalue7 = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'item'


class Player(models.Model):
    account_id = models.IntegerField()
    name = models.CharField(max_length=24)
    job = models.IntegerField()
    voice = models.IntegerField()
    dir = models.IntegerField()
    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField()
    map_index = models.IntegerField()
    exit_x = models.IntegerField()
    exit_y = models.IntegerField()
    exit_map_index = models.IntegerField()
    hp = models.BigIntegerField()
    mp = models.SmallIntegerField()
    stamina = models.SmallIntegerField()
    random_hp = models.SmallIntegerField()
    random_sp = models.SmallIntegerField()
    playtime = models.IntegerField()
    level = models.IntegerField()
    level_step = models.IntegerField()
    st = models.SmallIntegerField()
    ht = models.SmallIntegerField()
    dx = models.SmallIntegerField()
    iq = models.SmallIntegerField()
    exp = models.IntegerField()
    gold = models.BigIntegerField()
    stat_point = models.SmallIntegerField()
    skill_point = models.SmallIntegerField()
    quickslot = models.TextField(blank=True, null=True)
    ip = models.CharField(max_length=15, blank=True, null=True)
    part_main = models.IntegerField()
    part_base = models.IntegerField()
    part_hair = models.SmallIntegerField()
    part_acce = models.SmallIntegerField()
    skill_group = models.IntegerField()
    skill_level = models.TextField(blank=True, null=True)
    alignment = models.IntegerField()
    last_play = models.DateTimeField()
    change_name = models.IntegerField()
    mobile = models.CharField(max_length=24, blank=True, null=True)
    sub_skill_point = models.SmallIntegerField()
    stat_reset_count = models.IntegerField()
    horse_hp = models.SmallIntegerField()
    horse_stamina = models.SmallIntegerField()
    horse_level = models.IntegerField()
    horse_hp_droptime = models.IntegerField()
    horse_riding = models.IntegerField()
    horse_skill_point = models.SmallIntegerField()
    mymoney = models.BigIntegerField()
    ranking = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'player'

    def __unicode__(self):
        return self.name 


class PlayerDeleted(models.Model):
    account_id = models.IntegerField()
    name = models.CharField(max_length=24)
    job = models.IntegerField()
    voice = models.IntegerField()
    dir = models.IntegerField()
    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField()
    map_index = models.IntegerField()
    exit_x = models.IntegerField()
    exit_y = models.IntegerField()
    exit_map_index = models.IntegerField()
    hp = models.BigIntegerField()
    mp = models.SmallIntegerField()
    stamina = models.SmallIntegerField()
    random_hp = models.SmallIntegerField()
    random_sp = models.SmallIntegerField()
    playtime = models.IntegerField()
    level = models.IntegerField()
    level_step = models.IntegerField()
    st = models.SmallIntegerField()
    ht = models.SmallIntegerField()
    dx = models.SmallIntegerField()
    iq = models.SmallIntegerField()
    exp = models.IntegerField()
    gold = models.BigIntegerField()
    stat_point = models.SmallIntegerField()
    skill_point = models.SmallIntegerField()
    quickslot = models.TextField(blank=True, null=True)
    ip = models.CharField(max_length=15, blank=True, null=True)
    part_main = models.IntegerField()
    part_base = models.IntegerField()
    part_hair = models.SmallIntegerField()
    part_acce = models.SmallIntegerField()
    skill_group = models.IntegerField()
    skill_level = models.TextField(blank=True, null=True)
    alignment = models.IntegerField()
    last_play = models.DateTimeField()
    change_name = models.IntegerField()
    mobile = models.CharField(max_length=24, blank=True, null=True)
    sub_skill_point = models.SmallIntegerField()
    stat_reset_count = models.IntegerField()
    horse_hp = models.SmallIntegerField()
    horse_stamina = models.SmallIntegerField()
    horse_level = models.IntegerField()
    horse_hp_droptime = models.IntegerField()
    horse_riding = models.IntegerField()
    horse_skill_point = models.SmallIntegerField()
    mymoney = models.BigIntegerField()
    ranking = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'player_deleted'

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

