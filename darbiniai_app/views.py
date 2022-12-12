from django.shortcuts import render, redirect, get_object_or_404
from .forms import LeaderboardForm, LBEntryForm, MEEntryForm, GameForm

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.auth.models import User
from .forms import changeUsernameForm
from django.contrib.auth.forms import PasswordChangeForm as changePasswordForm

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from darbiniai_app.models import Leaderboard, Entry, Game
from darbiniai_app.serializers import LeaderboardSerializer, EntrySerializer
from rest_framework.decorators import api_view

# Create your views here.

# views'ai skirti nurodyti, kas ivyksta, kreipiantis i tam tikra URL su tam tikru html request'u

def index(request):
    """The home page for darbiniai_app"""
    return render(request, 'darbiniai_app/index.html')

# def admin(request):
#     """Manual request for admin page by button"""
#     return render(request, 'darbiniai_app/admin.html')


# book

def leaderboards(request):
    """show all leaderboards"""
    leaderboards = Leaderboard.objects.order_by('gameName')
    context = {'leaderboards': leaderboards}
    return render(request, 'darbiniai_app/leaderboards.html', context)

def entries(request, gameName):
    """show a single leaderboard and all its entries"""
    leaderboard = get_object_or_404(Leaderboard, gameName = gameName)
    entries = leaderboard.entry_set.order_by('-score')
    context = {'leaderboard': leaderboard, 'entries': entries}
    return render(request, 'darbiniai_app/entries.html', context)

@login_required
def my_entries(request):
    """show a logged in user's every entry"""
    leaderboards = Leaderboard.objects.all()
    myEntries = list()

    if leaderboards: # if there are leaderboards in the DB

        for leaderboard in leaderboards:
            entries = leaderboard.entry_set.filter(owner=request.user).order_by('-score')
            for entry in entries:
                myEntries.append(entry)

    else:
        leaderboard = None

    context = {'leaderboard': leaderboard, 'myEntries': myEntries, 'username':request.user}

    return render(request, 'darbiniai_app/my_entries.html', context)

@login_required
def new_leaderboard(request):
    """Add a new leaderboard"""
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

# from leaderboards/ 
@login_required
def LBnew_entry(request, gameName):
    """Add a new entry to a specified leaderboard from leaderboards/"""
    leaderboard = get_object_or_404(Leaderboard, gameName = gameName)

    if request.method != 'POST':
        #No data submitted; create blank form.
        form = LBEntryForm()
    else:
        #POST data submitted; process data.
        form = LBEntryForm(data = request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.LB = leaderboard
            new_entry.owner = request.user
            new_entry.save()
            return redirect('darbiniai_app:entries', gameName = gameName)

    #Display blank or invalid form.
    context = {'leaderboard': leaderboard, 'form': form}
    return render(request, 'darbiniai_app/LBnew_entry.html', context)

@login_required
def MEnew_entry(request):
    """Add a new entry to a leaderboard from my_entries/"""

    if request.method != 'POST':
        #No data submitted; create blank form.
        form = MEEntryForm()
    else:
        #POST data submitted; process data.
        form = MEEntryForm(data = request.POST)
        if form.is_valid():

            new_entry = form.save(commit=False)
            new_entry.owner = request.user
            new_entry.save()
            return redirect('darbiniai_app:my_entries')

    #Display blank or invalid form.
    context = {'form': form}
    return render(request, 'darbiniai_app/MEnew_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry"""
    entry = get_object_or_404(Entry, id=entry_id)

    if entry.owner != request.user and not request.user.is_superuser and not request.user.is_admin:
        raise Http404

    leaderboard = entry.LB

    if request.method != 'POST':
        #Initial request; pre-fill form with the current entry.
        form = LBEntryForm(instance=entry)
    else:
        #POST data submitted; process data.
        form = LBEntryForm(instance=entry, data = request.POST)
        if form.is_valid():
            form.save()

            return redirect('darbiniai_app:entries', gameName = leaderboard.gameName)

    context = {'entry':entry, 'leaderboard': leaderboard, 'form': form}
    return render(request, 'darbiniai_app/edit_entry.html', context)

# Account
@login_required
def account(request):
    """ Opens the account page. """
    user = request.user

    if request.method == 'GET':

        context = {'user':user, 'request':request}
        return render(request, 'darbiniai_app/account.html', context)

    else:
        raise Http404

@login_required
def change_username(request):
    """Allows user to change their username."""
    user = request.user

    if request.method != 'POST':

        form = changeUsernameForm()

    else:

        form = changeUsernameForm(instance = user, data = request.POST)

        if form.is_valid():
            form.save()

            return redirect('darbiniai_app:account')

    context = {'user':user, 'form': form}
    return render(request, 'darbiniai_app/change_username.html', context)


@login_required
def change_password(request):
    """Allows user to change their password."""
    user = request.user

    if request.method != 'POST':

        form = changePasswordForm(user=user)

    else:

        form = changePasswordForm(user=user, data = request.POST)

        if form.is_valid():
            form.save()

            return redirect('darbiniai_app:account')

    context = {'user':user, 'form': form}
    return render(request, 'darbiniai_app/change_password.html', context)
        
@login_required
def delete_account(request):
    """Allows user to delete their account."""
    user = request.user

    if request.method == 'GET':

        context = {'user':user}
        return render(request, 'darbiniai_app/delete_account.html', context)

    elif request.method == 'POST':

        request.user.delete()

        return redirect('darbiniai_app:account_deleted')

def account_deleted(request):
    """Redirects user after deleting their account."""

    if request.method == 'GET':

        return render(request, 'darbiniai_app/account_deleted.html')

# Files
def library (request):
    """Game library page."""
    if request.method == 'GET':

        games = Game.objects.all()

        context = {"games" : games}
        return render (request, 'darbiniai_app/library.html', context)


def add_game (request):
    """Add a game to the library."""
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect ('darbiniai_app:library' )
    else:
        form = GameForm()

    context = {"form": form}
    return render(request, 'darbiniai_app/add_game.html', context)


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