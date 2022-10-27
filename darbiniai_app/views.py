from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from darbiniai_app.models import Leaderboard
from darbiniai_app.serializers import LeaderboardSerializer
from rest_framework.decorators import api_view

# Create your views here.

def index(request):
    """The home page for darbiniai_app"""
    return render(request, 'darbiniai_app/index.html')


# book

def leaderboards(request):
    """show all leaderboards"""
    leaderboards = Leaderboard.objects.order_by('gameName')
    context = {'leaderboards': leaderboards}
    return render(request, 'darbiniai_app/leaderboards.html', context)

def entries(request, gameName):
    """show a single leaderboard and all its entries"""
    leaderboard = Leaderboard.objects.get(gameName = gameName)
    entries = leaderboard.entry_set.order_by('-score')
    context = {'leaderboard': leaderboard, 'entries': entries}
    return render(request, 'darbiniai_app/entries.html', context)


# API

@api_view(['GET', 'POST', 'DELETE'])
def leaderboard_list(request):
    # GET list of leaderboards, POST a new leaderboard, DELETE all leaderboards
    if request.method == 'GET':
        leaderboards = Leaderboard.objects.all()
        
        gameName = request.GET.get('gameName', None)
        if gameName is not None:
            leaderboards = leaderboards.filter(gameName__icontains=gameName)
        
        leaderboard_serializer = LeaderboardSerializer(leaderboards, many=True)
        return JsonResponse(leaderboard_serializer.data, safe=False)
        # 'safe=False' for objects serialization


    elif request.method == 'POST':
        leaderboard_data = JSONParser().parse(request)
        leaderboard_serializer = LeaderboardSerializer(data=leaderboard_data)
        if leaderboard_serializer.is_valid():
            leaderboard_serializer.save()
            return JsonResponse(leaderboard_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(leaderboard_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
    elif request.method == 'DELETE':
        count = Leaderboard.objects.all().delete()
        return JsonResponse({'message': '{} Leaderboards were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

 
@api_view(['GET', 'PUT', 'DELETE'])
def leaderboard_detail(request, gameName):
    # find leaderboard by pk (gameName)
    try: 
        leaderboard = Leaderboard.objects.get(gameName=gameName) 
        if request.method == 'GET': 
            leaderboard_serializer = LeaderboardSerializer(leaderboard) 
            return JsonResponse(leaderboard_serializer.data) 

        elif request.method == 'PUT': 
            leaderboard_data = JSONParser().parse(request) 
            leaderboard_serializer = LeaderboardSerializer(leaderboard, data=leaderboard_data) 
            if leaderboard_serializer.is_valid(): 
                leaderboard_serializer.save() 
                return JsonResponse(leaderboard_serializer.data) 
            return JsonResponse(leaderboard_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        
        elif request.method == 'DELETE': 
            leaderboard.delete() 
            return JsonResponse({'message': 'Leaderboard was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

    except Leaderboard.DoesNotExist: 
        return JsonResponse({'message': 'The leaderboard does not exist'}, status=status.HTTP_404_NOT_FOUND) 