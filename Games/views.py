from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
from .models import *
from django.db.models import Q
from Games.serializers import *
from rest_framework.decorators import api_view
from django.views.generic.base import TemplateView


from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage

import dateutil.parser


import datetime
from Games.functions import *


#### api to create profile or edit profile of user
@api_view(['post'])
def add_edit_user_profile(request):
    """
    parameters:
      - name: user_name
        description: Player Username
        required: false
        type: string
        paramType: form
      - name: user_email
        description: Player Email
        required: false
        type: string
        paramType: form
      - name: user_mobile
        description: Player Mobile
        required: false
        type: string
        paramType: form
      - name: profile_photo
        description: Profile Photo 
        required: false
        type: file
        paramType: form
      - name: user_country
        description: User Country
        required: false
        type: string
        paramType: form
      - name: user_pk
        description: pk of user - if created
        required: false
        type: string
        paramType: form

    """
    #### add edit user profile
    response = {}


    if "user_pk" in request.data:
        ### if editng previously created user
        game_user = Game_User.objects.get(pk = request.data["user_pk"], is_deleted = False)

    else:
        ### add new user
        game_user = Game_User()

    if "user_name" in request.data:
        game_user.user_name = request.data["user_name"]  ### username

    if "user_email" in request.data:
        game_user.user_email = request.data["user_email"] ### email

    if "user_mobile" in request.data:
        game_user.user_mobile = request.data["user_mobile"] ### mobile

    if "user_country" in request.data:
        game_user.user_country = request.data["user_country"] ### user country

    if "profile_photo" in request.data:
        game_user.profile_photo = request.data["profile_photo"] ### profile photo

    game_user.save()

    if "user_pk" in request.data:
        response["result"] = 1
        response["message"] = "Profile Of user updated successfully"

    else:
        response["result"] = 1
        response["message"] = "Profile Of user created successfully"

    return Response(response, status=status.HTTP_200_OK)



##### get user profile ###
@api_view(['post'])
def get_user_profile(request):
    """
    parameters:
      - name: user_pk
        description: pk of user
        required: true
        type: string
        paramType: form

    """
    response = {}
    user_pk = request.data["user_pk"]

    if Game_User.objects.filter(pk = user_pk, is_deleted = False).exists():
        game_user = Game_User.objects.get(pk = user_pk, is_deleted = False) ### get corresponding user


        game_user_serializer = UserDetailsSerializer(game_user, many = False).data ### sending data to serializer

        active_level = GameLevelsRankings.get_active_level(game_user) ### get active details of user

        if not active_level == None:
            game_user_serializer["current_score"] = active_level.level_score  ## current score
            game_user_serializer["level_ranking"] = active_level.level_ranking  ### level ranking
            game_user_serializer["overall_ranking"] = active_level.overall_ranking ### global ranking
            game_user_serializer["level_reached"] = active_level.level_reached.level_name ##level reached

        else:
            game_user_serializer["current_score"] = ""
            game_user_serializer["level_ranking"] = ""
            game_user_serializer["overall_ranking"] = ""
            game_user_serializer["level_reached"] = ""


        response["result"] = 1
        response["data"] = {
            "user_data" : game_user_serializer
        }

    else:
        response["result"] = 0
        response["errors"] = ["User Does Not Exists"]
        return Response(response, status=status.HTTP_200_OK)

    
    return Response(response, status=status.HTTP_200_OK)


########## get level rank and overall rank on completing the stage********
@api_view(['post'])
def calculate_rank_on_game_completion(request):
    """
    parameters:
      - name: user_pk
        description: pk of user
        required: true
        type: string
        paramType: form
      - name: points
        description: point scored in completing the level
        required: true
        type: string
        paramType: form
      - name: start_time
        description: start time taken to start the game - eg. yyyy-mm-ddTHH:MM:SSZ
        required: true
        type: string
        paramType: form
      - name: end_time
        description: end time taken to complete the game - eg.  yyyy-mm-ddTHH:MM:SSZ
        required: true
        type: string
        paramType: form

    """
    response = {}
    user_pk = request.data["user_pk"]
    points = request.data["points"] ### points scored
    users_with_same_score = []
    global_users_with_same_score = []
    game_level = None

    start_time = dateutil.parser.parse(request.data["start_time"]).replace(second=0, microsecond=0)
    end_time = dateutil.parser.parse(request.data["end_time"]).replace(second=0, microsecond=0)

    if end_time < start_time : #### SECURITY CHECK
        response["result"] = 0
        response["errors"] = ["Starting time of game is greater than end time of the game"]
        return Response(response, status=status.HTTP_200_OK)
    
    time_taken = (end_time - start_time).total_seconds()  #### in seconds

    if Game_User.objects.filter(pk = user_pk, is_deleted = False).exists(): ### check if user exists or not
        game_user = Game_User.objects.get(pk = user_pk, is_deleted = False)


        #### get all levels in a game

        if Game_Levels.objects.filter(min_score_assigned__lte = points, max_score_assigned__gte = points).exists():
            game_level = Game_Levels.objects.filter(min_score_assigned__lte = points, max_score_assigned__gte = points).order_by("-max_score_assigned")

            game_level = game_level[0] 

        else:
            response["result"] = 0
            response["errors"] = ["Please set the level score within the score given"]
            return Response(response, status=status.HTTP_200_OK)


        #### if previous rows of levels are created, deleting their rows to update a new score     
        if GameLevelsRankings.objects.filter(game_user = game_user, active = True).exists():
            previous_rankings_of_corresponding_user = GameLevelsRankings.objects.filter(game_user = game_user, active = True)

            for a_previous_rankings_of_corresponding_user in previous_rankings_of_corresponding_user:
                a_previous_rankings_of_corresponding_user.active = False
                a_previous_rankings_of_corresponding_user.save()

        #### create a new game level row to update the recent one ######
        user_game_level = GameLevelsRankings()
        user_game_level.game_user = game_user
        user_game_level.level_reached = game_level
        user_game_level.level_score = points
        user_game_level.time_taken = time_taken
        user_game_level.active = True
        user_game_level.save()

        ##### excluding the current user , we are getting all other users data, this array is useful at all the place in current api ######
        global_level_rankings = GameLevelsRankings.objects.filter(active = True).exclude(game_user = game_user).order_by("-level_score")




        #### to calculate stage level rank score based on the points scored

        all_stage_level_rankings = global_level_rankings.filter(level_reached = game_level, level_score__lte = points).order_by("-level_score")

        ###### to get previous level rank user prior to corressponding user, if exists
        if global_level_rankings.filter(level_reached = game_level, level_score__gt = points).order_by("-level_ranking").exists():

            previous_user_stage_ranking = global_level_rankings.filter(level_reached = game_level, level_score__gt = points).order_by("-level_ranking")[0].level_ranking

        else:
            previous_user_stage_ranking = 0

        ######## if user rank lies in between the other user, calculate rank using this logic
        if len(all_stage_level_rankings) > 0:
           
            user_game_level.level_ranking = previous_user_stage_ranking + 1 ### add corressponding user rank of previous one
            user_game_level.save()


            #### if the user with same level score exists ???
            if all_stage_level_rankings.filter(level_score = points).exists():
                users_with_same_score = all_stage_level_rankings.filter(level_score = points, time_taken__gt = time_taken).order_by("time_taken") ### compared by time

                for a_user_with_same_score in users_with_same_score:
                    a_user_with_same_score.level_ranking += 1  ### increment other user rank incrementally by 1 whose score is less than other user
                    a_user_with_same_score.save() 


            all_stage_level_rankings.exclude(pk__in = users_with_same_score) ### exclude the other users with same level point score, refer above process

            for a_level_user in all_stage_level_rankings:

                a_level_user.level_ranking += 1
                a_level_user.save() 


        else:
            ##### if no user has less rank prior to corresponding user

            if global_level_rankings.filter(level_reached = game_level, level_score__gt = points).exists(): 
                user_game_level.level_ranking = previous_user_stage_ranking + 1
                user_game_level.save()

            else:
                user_game_level.level_ranking = 1 ### used for first entry 
                user_game_level.save()





        #### to calculate global rank score based on the points scored

        all_game_level_rankings = global_level_rankings.filter(level_score__lte = points).order_by("-level_score")

        ###### to get previous global rank user prior to corressponding user, if exists
        if global_level_rankings.filter(level_score__gt = points).order_by("-overall_ranking").exists():
            previous_user_overall_ranking = global_level_rankings.filter(level_score__gt = points).order_by("-overall_ranking")[0].overall_ranking
        else:
            previous_user_overall_ranking = 0


         ######## if user rank lies in between the other user, calculate rank using this logic
        if len(all_game_level_rankings) > 0:

            
            user_game_level.overall_ranking = previous_user_overall_ranking + 1 ### add corressponding user rank of previous one
            user_game_level.save()

            #### if the user with same global score exists ???
            if all_game_level_rankings.filter(level_score = points).exists():
                global_users_with_same_score = all_game_level_rankings.filter(level_score = points, time_taken__gt = time_taken).order_by("time_taken") ### compared by time

                for a_user_with_same_score in global_users_with_same_score: ### increment other user rank incrementally by 1 whose score is less than other user
                    a_user_with_same_score.overall_ranking +=1
                    a_user_with_same_score.save() 

            all_game_level_rankings.exclude(pk__in = global_users_with_same_score) ### exclude the other users with same point score, refer above process

            for a_global_user in all_game_level_rankings:
                a_global_user.overall_ranking += 1
                a_global_user.save() 

        else:
            ##### if no user has less rank prior to corresponding user
            if global_level_rankings.filter(level_score__gt = points).exists():
                previous_user_ranking = global_level_rankings.filter(level_score__gt = points).order_by("-overall_ranking")[0]
                user_game_level.overall_ranking = previous_user_overall_ranking + 1
                user_game_level.save()

            else:
                user_game_level.overall_ranking = 1 ### first entry
                user_game_level.save()

        response["result"] = 1
        response["message"] = "Your current level is " +str(user_game_level.level_reached.level_name) + " and your rank in terms of level is " +str(user_game_level.level_ranking) + " and your overall ranking is " +str(user_game_level.overall_ranking)+ "."
        
    else:
        response["result"] = 0
        response["errors"] = ["User Does Not Exists"]
        return Response(response, status=status.HTTP_200_OK)

    return Response(response, status=status.HTTP_200_OK)


#### script to calculate weekly progress of the user - game played during that time ######

#### Instead of api, cron job would be the correct place to implement the logic, but the only difference would be transfer this function into shell #####
@api_view(['post'])
def script_to_mail_weekly_progress(request):
    """

    """

    response = {}

    todays_date = datetime.datetime.now() ###get todays date
    day = todays_date.strftime("%A") ### get week day

    d = todays_date - timedelta(days=7) ### caclculating days difference

    from_date = d.replace(hour = 18, minute = 0, second = 0, microsecond = 0) ### last week saturday 6 pm
    to_date = todays_date.replace(hour = 18, minute = 0, second = 0, microsecond = 0) ### today saturday 6 pm

    # if day == "Saturday" and todays_date == to_date:
    if day == "Sunday": 
        all_game_users = Game_User.objects.filter(is_deleted = False) ### filter deleted users

        for a_user in all_game_users:

            ### active user levels during that time period
            if GameLevelsRankings.objects.filter(game_user = a_user, active = True, created_at__range = [from_date, to_date]).exists():
                active_level = GameLevelsRankings.objects.filter(game_user = a_user, active = True, created_at__range = [from_date, to_date]).order_by("-created_at")[0]
            else:
                active_level = None

            #### if game played during that time ??
            if not active_level == None:
                if active_level.game_user.user_email:   #### check if the email has been updated in user profile
                    sub = "No-Reply: User Ranking System Daily Updates"

                    object_to_send = {
                        "user_name": active_level.game_user.user_name, ### username
                        'current_score': active_level.level_score, ### current score
                        'current_level_ranking': active_level.level_ranking, ## level ranking
                        'overall_ranking': active_level.overall_ranking, ### overall ranking
                        'level_reached': active_level.level_reached.level_name, ### current active level / stage
                        'from_date': from_date.date(), ### from date of last week
                        'to_date': to_date.date() ### todays date i.e. saturday 6 pm

                    }

                    ### get template and render the object
                    msg = get_template('emailers/user_weekly_updates.html').render(object_to_send)

                    to = [active_level.game_user.user_email] #### email of the user
                    html_mail(sub, msg, to) ### mail function


        response["message"] = "Mails have been sent successfully to the user"

    response["result"] = 1

    return Response(response, status=status.HTTP_200_OK)
