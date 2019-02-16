from rest_framework import serializers
from Games.models import *

class UserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game_User
        fields = (
            'pk' , 
            'user_name', 
            'user_email', 
            'user_mobile',
            'profile_photo',
            'current_level',
            'is_deleted',
        )