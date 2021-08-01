from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile,CycleOnRoad,Cycle
from django.contrib.auth.models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id","username","first_name","last_name","email"]
class ProfileSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model = Profile
        fields = '__all__'
class CycleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cycle
        fields="__all__"
class RideSerializer(serializers.ModelSerializer):
    cycle=CycleSerializer()
    class Meta:
        model=CycleOnRoad
        fields="__all__"