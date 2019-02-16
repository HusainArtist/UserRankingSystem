from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
from .models import *
from django.db.models import Q
from Games.serializers import *
from rest_framework.decorators import api_view
from django.views.generic.base import TemplateView

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
      - name: user_pk
        description: pk of user
        required: false
        type: string
        paramType: form

    """
    #### add edit user profile
    response = {}

    if "user_pk" in request.data:

        game_user = Game_User.objects.get(pk = request.data["user_pk"], is_deleted = False)

    else:

        game_user = Game_User()

    if "user_name" in request.data:
        game_user.user_name = request.data["user_name"]

    if "user_email" in request.data:
        game_user.user_email = request.data["user_email"]

    if "user_mobile" in request.data:
        game_user.user_mobile = request.data["user_mobile"]


    if "profile_photo" in request.data:
        game_user.profile_photo = request.data["profile_photo"]

    game_user.save()

    if "user_pk" in request.data:
        response["result"] = 1
        response["message"] = "Profile Of user updated successfully"


    else:
        response["result"] = 1
        response["message"] = "Profile Of user created successfully"


    return Response(response, status=status.HTTP_200_OK)




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
    ### add edit user profile
    response = {}
    user_pk = request.data["user_pk"]

    if Game_User.objects.filter(pk = user_pk, is_deleted = False).exists():
        game_user = Game_User.objects.get(pk = user_pk, is_deleted = False)


        game_user_serializer = UserDetailsSerializer(game_user, many = False).data

        response["result"] = 1
        response["data"] = {
            "user_data" : game_user_serializer
        }

    else:
        response["result"] = 0
        response["errors"] = ["User Does Not Exists"]
        return Response(response, status=status.HTTP_200_OK)

    

    return Response(response, status=status.HTTP_200_OK)





    # ######### calculate rank for one particular stage ********
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
      - name: time_taken
        description: time taken to complete the level - (in seconds)
        required: true
        type: string
        paramType: form

    """
    response = {}
    user_pk = request.data["user_pk"]
    points = request.data["points"]
    time_taken = request.data["time_taken"]
    game_level = None

    if Game_User.objects.filter(pk = user_pk, is_deleted = False).exists():
        game_user = Game_User.objects.get(pk = user_pk, is_deleted = False)


        all_game_levels = Game_Levels.objects.all()
        print (all_game_levels, "all_game_levels")

        for a_level in all_game_levels:
            print (a_level.min_score_assigned)
            print (a_level.max_score_assigned)
            print (points)

            if int(a_level.min_score_assigned) < int(points) and int(a_level.max_score_assigned) > int(points):
                game_level = a_level
                break;

        if game_level == None:
            response["result"] = 0
            response["errors"] = ["Please set the level score within the score given"]
            return Response(response, status=status.HTTP_200_OK)

        # if Game_Levels.objects.filter(Q(min_score_assigned__lte = points) & Q(max_score_assigned__gte = points)).exists():
        #     game_level = Game_Levels.objects.filter(Q(min_score_assigned__lte = points) & Q(max_score_assigned__gte = points)).order_by("-max_score_assigned")
        #     print (game_level, "game_level")

        #     game_level = game_level[0] 

        # else:
        #     response["result"] = 0
        #     response["errors"] = ["Please set the level score within the score given"]
        #     return Response(response, status=status.HTTP_200_OK)

        user_game_level = GameLevelsRankings.objects.get(pk = 11)
        user_game_level.game_user = game_user
        user_game_level.level_reached = game_level
        user_game_level.level_score = points
        user_game_level.time_taken = time_taken
        user_game_level.active = True
        user_game_level.save()

        global_level_rankings = GameLevelsRankings.objects.all().exclude(game_user = game_user).order_by("-level_score")


        all_game_level_rankings = global_level_rankings.filter(level_reached = game_level, level_score__lte = points, active = True).order_by("-level_score")


        if len(all_game_level_rankings) > 0:
            if all_game_level_rankings.filter(level_score = points).exists():
                users_with_same_score = all_game_level_rankings.filter(level_score = points, time_taken__gte = time_taken).order_by("time_taken")

                for a_user_with_same_score in users_with_same_score:
                    a_user_with_same_score.level_ranking +=1
                    a_user_with_same_score.save() 


            for a_game_level in all_game_level_rankings:

                a_game_level.level_ranking += 1
                a_user_with_same_score.save() 




        else:
            if global_level_rankings.filter(level_reached = game_level, level_score__gt = points, active = True).exists():
                previous_user_ranking = global_level_rankings.filter(level_reached = game_level, level_score__gt = points, active = True).order_by("-ranking")[0]
                user_game_level.level_ranking = previous_user_ranking.ranking + 1
                user_game_level.save()

            else:
                user_game_level.level_ranking = 1
                user_game_level.save()


        if global_level_rankings.filter(level_score__gt = points, active = True).exists():
            previous_user_ranking = global_level_rankings.filter(level_score__gt = points, active = True).order_by("-ranking")[0]
            user_game_level.overall_ranking = previous_user_ranking.ranking + 1
            user_game_level.save()

        else:
            user_game_level.overall_ranking = 1
            user_game_level.save()








        response["result"] = 1
        

    else:
        response["result"] = 0
        response["errors"] = ["User Does Not Exists"]
        return Response(response, status=status.HTTP_200_OK)

    return Response(response, status=status.HTTP_200_OK)




