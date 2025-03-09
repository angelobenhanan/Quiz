from rest_framework import serializers
from .models  import*

class TryoutSerializer(serializers.ModelSerializer):
    class Meta():
        model = Tryout
        fields = "__all__"

class QuestionSerializer(serializers.ModelSerializer):
    class Meta():
        model = Question
        fields = "__all__"