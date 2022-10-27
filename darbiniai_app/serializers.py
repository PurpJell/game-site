from rest_framework import serializers 
from darbiniai_app.models import Leaderboard
 
 
class LeaderboardSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Leaderboard
        fields = ('gameName',
                  'date_added',)