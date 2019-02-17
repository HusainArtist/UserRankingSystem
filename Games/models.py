# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
from datetime import timedelta
from django.core.files.storage import FileSystemStorage

from django.core.files import File

from django.contrib.auth.models import User

fs = FileSystemStorage(location='media/') ### to store profile photo



#### will be set default by admin user ######
class Game_Levels(models.Model):

	level_name = models.CharField(max_length=200, blank = True, null=True)  ### level name
	min_score_assigned = models.FloatField(blank = True, null=True) ### min score assigned
	max_score_assigned = models.FloatField(blank = True, null=True) ### max score assigned
	created_at = models.DateTimeField(null=True, blank=True, default=datetime.datetime.now)

	def __str__(self):
	    return str(self.level_name)

	class Meta:
	    verbose_name_plural = "Game Levels"


	##### EXAMPLE ######

	#### level name = LEVEL 1     min_score = 0      max_score = 100 ####
	#### level name = LEVEL 2     min_score = 101    max_score = 200 ####

###### User Profile Model ##########
class Game_User(models.Model):

    user_name = models.CharField(max_length=200, blank = True, null=True)
    user_email = models.CharField(max_length=40, blank = True, null=True)
    user_mobile = models.CharField(max_length=40, blank = True, null=True)
    user_country = models.CharField(max_length=40, blank = True, null=True)  ### country /place where user belongs
    profile_photo = models.FileField(storage=fs, upload_to = 'profile_photo/', blank = True, null = True)
                            
    is_deleted = models.BooleanField(default = False) ### to identify deleted user
    created_at = models.DateTimeField(null=True, blank=True, default=datetime.datetime.now) #### when was user created ??

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name_plural = "Game User"



###### Game Level Tracking Model ########## - whenever the score gets created a new row will be created in this table
class GameLevelsRankings(models.Model):
	game_user = models.ForeignKey(Game_User, blank = True, null = True)   ### foreign key of user
	level_reached = models.ForeignKey(Game_Levels, blank = True, null = True) ###level reached
	level_ranking = models.IntegerField(blank = True, null=True) ### level wise ranking
	overall_ranking  = models.IntegerField(blank = True, null=True) ###overall ranking
	level_score = models.FloatField(max_length=200, blank = True, null=True)  ### current score
	time_taken = models.FloatField(max_length=20, blank = True, null=True) ### time difference in seconds
	active = models.BooleanField(default = False) ###used to identify most recent row in a table

	created_at = models.DateTimeField(null=True, blank=True, default=datetime.datetime.now)


	#### function to get most active score/row of user requested
	def get_active_level(game_user):
		if GameLevelsRankings.objects.filter(game_user = game_user, active = True).exists():
			return GameLevelsRankings.objects.get(game_user = game_user, active = True)
		else:
			return None

	def __str__(self):
	    return str(self.game_user) + "-" + str(self.level_reached.level_name)

	class Meta:
	    verbose_name_plural = "Game Level Rankings"



