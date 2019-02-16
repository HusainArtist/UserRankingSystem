# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime

from storages.backends.s3boto import S3BotoStorage
from django.core.files.storage import FileSystemStorage

from django.core.files import File

from django.contrib.auth.models import User

fs = FileSystemStorage(location='media/')

class S3CustomStorage(S3BotoStorage):
    def _normalize_name(self, name):
        """
        Get rid of this crap: http://stackoverflow.com/questions/12535123/django-storages-and-amazon-s3-suspiciousoperation
        """
        return name


class Game_Levels(models.Model):

	level_name = models.CharField(max_length=200, blank = True, null=True)
	min_score_assigned = models.CharField(max_length=200, blank = True, null=True)
	max_score_assigned = models.CharField(max_length=200, blank = True, null=True)
	created_at = models.DateTimeField(null=True, blank=True, default=datetime.datetime.now)


class Game_User(User):

    # user_name = models.CharField(max_length=200, blank = True, null=True)
    # user_email = models.CharField(max_length=40, blank = True, null=True)
    user_mobile = models.CharField(max_length=20, blank = True, null=True)

    profile_photo = models.FileField(storage=fs, upload_to = 'profile_photo/', blank = True, null = True)
    current_level = models.ForeignKey(Game_Levels, blank = True, null = True)

                                
    is_deleted = models.BooleanField(default = False)
    created_at = models.DateTimeField(null=True, blank=True, default=datetime.datetime.now)



class GameLevelsRankings(models.Model):
	game_user = models.ForeignKey(Game_User, blank = True, null = True)
	level_reached = models.ForeignKey(Game_Levels, blank = True, null = True)
	level_ranking = models.CharField(max_length=200, blank = True, null=True)
	overall_ranking  = models.CharField(max_length=200, blank = True, null=True)
	level_score = models.CharField(max_length=200, blank = True, null=True)
	time_taken = models.CharField(max_length=20, blank = True, null=True)
	created_at = models.DateTimeField(null=True, blank=True, default=datetime.datetime.now)



# class GameOverallRankingData(models.Model):

# 	game_users = models.ForeignKey(Game_User, blank = True, null = True)
# 	won = models.BooleanField(default = True)
# 	level_reached = models.ForeignKey(Game_Levels, blank = True, null = True)
# 	level_score = models.CharField(max_length=200, blank = True, null=True)
# 	created_at = models.DateTimeField(null=True, blank=True, default=datetime.datetime.now)

# Create your models here.
