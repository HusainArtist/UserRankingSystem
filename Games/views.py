from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
from .models import *
from rest_framework.decorators import api_view
from django.views.generic.base import TemplateView

@api_view(['post'])
def search_by_prefix(request):
    """
    parameters:
      - name: word
        description: type any word 
        required: true
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


    if "user_mobile" in request.data:
        game_user.user_mobile = request.data["user_mobile"]

    if "user_mobile" in request.data:
        game_user.user_mobile = request.data["user_mobile"]


    game_user.save()



    ###### get profile data


    # response = {}
    # user_pk = request.data["user_pk"]

    # if Game_User.objects.filter(pk = user_pk, is_deleted = False).exists():
    #     game_user = Game_User.objects.get(pk = user_pk, is_deleted = False)


    #     response["result"] = 1
    #     response["data"] = {
    #         "user_data" = game_user_serializer
    #     }

    # else:
    #     response["result"] = 0
    #     response["errors"] = ["User Does Not Exists"]
    #     return Response(response, status=status.HTTP_200_OK)


    # ######### calculate rank for one particular stage ********



    # response = {}
    # points = request.data["points"]
    # time_taken = request.data["time_taken"]

    # if Game_User.objects.filter(pk = user_pk, is_deleted = False).exists():
    #     game_user = Game_User.objects.get(pk = user_pk, is_deleted = False)

    #     if Game_Levels.objects.filter(Q(min_score_assigned__gte = points) | Q(max_score_assigned__lte = points)).exists():
    #         game_level = Game_Levels.objects.filter(Q(min_score_assigned__gte = points) | Q(max_score_assigned__lte = points))[0]

    #     else:
    #         response["result"] = 0
    #         response["errors"] = ["Please set the level score within the score given"]
    #         return Response(response, status=status.HTTP_200_OK)

    #     user_game_level = GameLevelsRankings()
    #     user_game_level.game_users = game_user
    #     user_game_level.level_reached = game_level
    #     user_game_level.level_score = points
    #     user_game_level.save()

    #     global_level_rankings = GameLevelsRankings.objects.all().exclude(game_users = game_user).order_by("level_score")


    #     all_game_level_rankings = GameLevelsRankings.objects.filter(level_reached = game_level, level_score__lte = points, game_user__current_level = game_level).exclude(game_users = game_user).order_by("level_score")

    #     if len(all_game_level_rankings) > 0:
    #         if all_game_level_rankings.filter(level_score = points).exists():
    #             users_with_same_score = all_game_level_rankings.filter(level_score = points, time_taken__lte = time_taken).order_by("time_taken")

    #             for a_user_with_same_score in users_with_same_score:
    #                 a_user_with_same_score.level_ranking +=1
    #                 a_user_with_same_score.save() 


    #         for a_game_level in all_game_level_rankings:

    #             a_game_level.level_ranking += 1
    #             a_user_with_same_score.save() 




    #     else:
    #         if global_level_rankings.filter(level_reached = game_level).exists()
    #             a_user_with_same_score.




    #     response["result"] = 1
        

    # else:
    #     response["result"] = 0
    #     response["errors"] = ["User Does Not Exists"]
    #     return Response(response, status=status.HTTP_200_OK)





