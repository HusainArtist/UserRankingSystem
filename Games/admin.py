from __future__ import unicode_literals

from django.contrib import admin

from Games.models import *

##### function to flter rows in table
def custom_titled_filter(title):
   class Wrapper(admin.FieldListFilter):
       def __new__(cls, *args, **kwargs):
           instance = admin.FieldListFilter.create(*args, **kwargs)
           instance.title = title
           return instance
   return Wrapper


class Game_UserAdmin(admin.ModelAdmin):
    model = Game_User
    list_display = ['pk' , 'user_name' , 'user_email' , 'user_mobile' , 'user_country' , 'is_deleted' , 'created_at']


class Game_LevelAdmin(admin.ModelAdmin):
    model = Game_Levels
    list_display = ['pk' , 'level_name' , 'min_score_assigned' , 'max_score_assigned' , 'created_at']


class GameLevelsRankingsAdmin(admin.ModelAdmin):
    model = GameLevelsRankings
    list_display = ['pk' , 'game_user' , 'level_reached' , 'level_score' , 'time_taken' , 'level_ranking' , 'overall_ranking' , 'active' , 'created_at']

    list_filter = [
    	('game_user', custom_titled_filter('--Game User--')),    
      ('level_reached__level_name', custom_titled_filter('--Levels--')),  
      ('active', custom_titled_filter('--Active--')),        
    ]
    search_fields = ['level_ranking', 'overall_ranking']


admin.site.register(Game_User, Game_UserAdmin)
admin.site.register(Game_Levels, Game_LevelAdmin)
admin.site.register(GameLevelsRankings, GameLevelsRankingsAdmin)

# Register your models here.
