from rest_framework import serializers 
from darbiniai_app.models import Leaderboard, Entry
 
 
 #serializeriai skirti darbui su API
class LeaderboardSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Leaderboard
        fields = ('gameName',
                  'date_added',)

class EntrySerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Entry
        fields = ('LB',
                  'owner',
                  'username',
                  'score',
                  'date_added',)