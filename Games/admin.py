# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
# from super_inlines.admin import SuperInlineModelAdmin, SuperModelAdmin

from Games.models import *


class Game_UserAdmin(admin.ModelAdmin):
    model = Game_User
    list_display = ['pk' , 'user_name' , 'user_email' , 'user_mobile' , 'is_deleted' , 'created_at']

class Game_LevelAdmin(admin.ModelAdmin):
    model = Game_Levels
    list_display = ['pk' , 'level_name' , 'min_score_assigned' , 'max_score_assigned' , 'created_at']

class GameLevelsRankingsAdmin(admin.ModelAdmin):
    model = GameLevelsRankings
    list_display = ['pk' , 'game_user' , 'level_reached' , 'level_score' , 'time_taken' , 'level_ranking' , 'overall_ranking' , 'active' , 'created_at']


admin.site.register(Game_User, Game_UserAdmin)
admin.site.register(Game_Levels, Game_LevelAdmin)
admin.site.register(GameLevelsRankings, GameLevelsRankingsAdmin)

# Register your models here.
