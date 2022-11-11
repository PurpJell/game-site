from django.shortcuts import render, redirect
from .forms import LeaderboardForm, EntryForm

from django.contrib.auth.decorators import login_required

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from darbiniai_app.models import Leaderboard, Entry
from darbiniai_app.serializers import LeaderboardSerializer, EntrySerializer
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

@login_required
def my_entries(request):
    """show a logged in user's every entry"""
    leaderboards = Leaderboard.objects.all()
    myEntries = list()
    for leaderboard in leaderboards:
        entries = leaderboard.entry_set.filter(owner=request.user)
        for entry in entries:
            myEntries.append(entry)
    context = {'leaderboard': leaderboard, 'myEntries': myEntries, 'username':request.user}
    return render(request, 'darbiniai_app/my_entries.html', context)

@login_required
def new_leaderboard(request):
    """Add a new leadeerboard"""
    if request.method != 'POST':
        # no data submitted; create a blank form.
        form = LeaderboardForm()
    else:
        # POST data submitted; process data.
        form = LeaderboardForm(data = request.POST)
        if form.is_valid():
            form.save()
            return redirect('darbiniai_app:leaderboards')

    context = {'form': form}
    return render(request, 'darbiniai_app/new_leaderboard.html', context)

@login_required
def new_entry(request, gameName):
    """Add a new entry to a specified leaderboard"""
    leaderboard = Leaderboard.objects.get(gameName = gameName)

    if request.method != 'POST':
        #No data submitted; create blank form.
        form = EntryForm()
    else:
        #POST data submitted; process data.
        form = EntryForm(data = request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.LB = leaderboard
            new_entry.save()
            return redirect('darbiniai_app:entries', gameName = gameName)

    #Display blank or invalid form.
    context = {'leaderboard': leaderboard, 'form': form}
    return render(request, 'darbiniai_app/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry"""
    entry = Entry.objects.get(id=entry_id)
    leaderboard = entry.LB

    if request.method != 'POST':
        #Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        #POST data submitted; process data.
        form = EntryForm(instance=entry, data = request.POST)
        if form.is_valid():
            form.save()
            return redirect('darbiniai_app:entries', gameName = leaderboard.gameName)

    context = {'entry':entry, 'leaderboard': leaderboard, 'form': form}
    return render(request, 'darbiniai_app/edit_entry.html', context)



# API

#Leaderboards

@api_view(['GET', 'POST', 'DELETE'])
def leaderboard_list(request):
    # GET list of leaderboards, POST a new leaderboard, DELETE all leaderboards
    if request.method == 'GET':
        leaderboards = Leaderboard.objects.all()
        
        #possibility to sort by name (if it contains a string specified (leaderboards/gameName=<string>))
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

        leaderboards = Leaderboard.objects.all()
        
        gameName = request.GET.get('gameName', None)
        if gameName is not None:
            leaderboards = leaderboards.filter(gameName__icontains=gameName)

        count = leaderboards.all().delete()
        return JsonResponse({'message': '{} Leaderboards were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

# CURRENTLY USELESS
# @api_view(['GET', 'PUT', 'DELETE'])
# def leaderboard_detail(request, gameName):
#     # find leaderboard by pk (gameName)
#     try: 
#         leaderboard = Leaderboard.objects.get(gameName=gameName) 
#         if request.method == 'GET': 
#             leaderboard_serializer = LeaderboardSerializer(leaderboard) 
#             return JsonResponse(leaderboard_serializer.data) 

#         elif request.method == 'PUT': 
#             leaderboard_data = JSONParser().parse(request) 
#             leaderboard_serializer = LeaderboardSerializer(leaderboard, data=leaderboard_data) 
#             if leaderboard_serializer.is_valid(): 
#                 leaderboard_serializer.save() 
#                 return JsonResponse(leaderboard_serializer.data) 
#             return JsonResponse(leaderboard_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        
#         elif request.method == 'DELETE': 
#             leaderboard.delete() 
#             return JsonResponse({'message': 'Leaderboard was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

#     except Leaderboard.DoesNotExist: 
#         return JsonResponse({'message': 'The leaderboard does not exist'}, status=status.HTTP_404_NOT_FOUND) 

# Entries

@api_view(['GET', 'POST', 'DELETE'])
def entry_list(request):
    # GET list of entries, POST a new entry, DELETE all entries
    if request.method == 'GET':
        entries = Entry.objects.all()
        
        username = request.GET.get('username', None)
        if username is not None:
            entries = entries.filter(username__icontains=username)
        
        entry_serializer = EntrySerializer(entries, many=True)
        return JsonResponse(entry_serializer.data, safe=False)
        # 'safe=False' for objects serialization


    elif request.method == 'POST':
        entry_data = JSONParser().parse(request)
        entry_serializer = EntrySerializer(data=entry_data)
        if entry_serializer.is_valid():
            entry_serializer.save()
            return JsonResponse(entry_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(entry_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
    elif request.method == 'DELETE':

        entries = Entry.objects.all()
        username = request.GET.get('username', None)
        if username is not None:
            entries = entries.filter(username__icontains=username)

        count = entries.all().delete()
        return JsonResponse({'message': '{} Entries were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)