from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *

class UserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)
    phone = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'phone',
            'first_name',
            'last_name',
            'current_level',
            'hidden_on_leaderboard',
            'id',
            'keys',
            'is_rigged',
            'machine_used',
        ]

    def create(self,data):
        user = User.objects.create(
            username = data['username'],
            email = data['email'],
            # first_name=data['first_name'],
            # last_name = data['last_name']
        )
        user.set_password(data['password'])
        user.save()
        return user

class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        exclude = ['answer','paidHint','keywords','rigword']

class TimerSerializer(ModelSerializer):
    class Meta:
        model = Timer
        fields = ['time','is_started','is_ended']

class FeedbackSerializer(ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'