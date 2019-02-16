# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from Games.models import *


admin.site.register(Game_User)
admin.site.register(Game_Levels)
admin.site.register(GameLevelsRankings)

# Register your models here.
