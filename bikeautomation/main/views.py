from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User
from .validators import email_validator,name_validator,phone_validator,nic_validator
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProfileSerializer,RideSerializer
from .models import Profile,Card,CycleOnRoad,Cycle,Complain,Feedback
import time
from django.contrib.auth import login, logout,authenticate
from .rider import Rider
from datetime import datetime,timezone
import pytz

# Create your views here.
def index(request):
    return HttpResponse("Hello")
# @csrf_exempt
class ProfileList(generics.ListCreateAPIView): # for just GET POST request
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ProfileDetails(generics.RetrieveUpdateDestroyAPIView): # for just GET POST request
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
@csrf_exempt
def signup(request):

    full_name= request.POST.get("fullname")
    print(full_name)
    if name_validator(full_name) == False:
        return JsonResponse({"message":"Invalid name"},status=400)
    email=request.POST.get("email")
    if email_validator(email) == False:
        return JsonResponse({"message":"Invalid email"},status=400)
    username=request.POST.get("username")
    contact=request.POST.get("phone")
    if phone_validator(contact) == False:
        return JsonResponse({"message":"Invalid phone number"},status=400)
    password=request.POST.get("password")
    print(password)
    nic=request.POST.get("nic")
    if nic_validator(nic) == False:
        return JsonResponse({"message":"Invalid nic"},status=400)
    full_name= full_name.split(" ")
    if len(full_name) <=2:
        first_name=full_name[0]
        last_name=full_name[1]
    else:
        first_name=''
        for i in range(len(full_name)-2):
            first_name+=f"{full_name[i]} "
        last_name= full_name[-1]
    try:
        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            

        )
        user.set_password(password)
        user.save()
    except:
        return JsonResponse({"message":"User already exists"},status=400)
    profile=Profile.objects.create(
        user=user,
        nic=nic,
        phone=contact
    )
    return JsonResponse({"user":username},status=201)
@csrf_exempt
def Login(request):
    username=request.POST.get("username")
    password=request.POST.get("password")
    user=authenticate(request,username=username,password=password)
    if user is not None:
        login(request,user)
        return JsonResponse ({"user":username},status=200)
    else:
        return JsonResponse({"message":"Invalid username or password"},status=400)
@csrf_exempt
def RideNow(request):
    username=request.POST.get("username")
    password=request.POST.get("password")
    user=authenticate(request,username=username,password=password)
    if user:
        active_ride=CycleOnRoad.objects.filter(status=1,card=user.profile.card)
        available_cycles=Cycle.objects.filter(status="N")
        if len(active_ride)>0 or len(available_cycles) ==0 or user.profile.balance<=-50:
            print("active rides already")
            return HttpResponse(status=400) 
        initial_time= time.time()
        global current_rider
        current_rider=Rider(user.username,initial_time)
        return HttpResponse(status=200)
    else:
        print("wrong pass")
        return HttpResponse(status=400)
@csrf_exempt    
def Verifycard(request,card_num):
    
    
    card= card_num
    try:
        card= Card.objects.get(card_no=card)
    except:
        return JsonResponse({"message":"Card not verified"},status=400)
    card_history=CycleOnRoad.objects.filter(card=card)
    try:
        last_ride=card_history.last().status
    except:
        last_ride=3
    if  last_ride==0 or len(card_history)==0:
        global current_rider
        try:
            current_rider=current_rider
        except:
            return JsonResponse({"message":"Timeout"},status=400)
        
        final_time=time.time()

        if final_time- current_rider.time <=100:
            print("not timeout")
            available_cycles=Cycle.objects.filter(status="N")
            cycle_history=CycleOnRoad.objects.last()

            if cycle_history:
                print("from history")
                for i in available_cycles:
                    print(i.no)
                    cycle=i
                    # if i != cycle_history.cycle:
                    #     cycle=i
                    #     break
            else:
                print("selecting first")
                cycle=available_cycles[0]
            ride =CycleOnRoad.objects.create(cycle=cycle,card=card,status=1)
            cycle.status="A"
            cycle.save()
            return JsonResponse({"message":"Ride started"},status=201)
        else:
            return JsonResponse({"message":"Timeout"},status=400)
    else:
        global current_rider_for_end
        try:
            rider_to_end= current_rider_for_end
        except:
            return JsonResponse({"message":"You haven't initiaited from application"},status=400)
        if time.time() -rider_to_end.time <=100: 
            rides=CycleOnRoad.objects.filter(card=card,status=1)
            for ride in rides:
                user=Profile.objects.get(card=card).user
                end_time=datetime.now(pytz.timezone('Asia/Karachi'))
                diff=(end_time-ride.starting_time).total_seconds()
                print(f"difference is {diff}")
                
                time_in_points= diff/60
                #The 3 in cost=time_in_points*3 says the cost of each min is 3rs, change the value to make a new rate
                cost= time_in_points*4
                user.profile.balance-=cost
                user.profile.save()
                ride.difference=diff
                ride.end_time=end_time
                ride.charge=cost
                ride.status=0
                ride.cycle.status="N"
                ride.cycle.save()
                ride.save()
            return HttpResponse(status=201)
        else:
            return JsonResponse({"message":"timeout"},status=400)

@csrf_exempt
def GetRideStatus(request):
    username=request.POST.get("username")
    password=request.POST.get("password")
    user=authenticate(request,username=username,password=password)
    if user:
        card=user.profile.card
        try:
            ride=CycleOnRoad.objects.get(card=card,status=1)
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=400)

# class RideList(generics.ListCreateAPIView,request): # for just GET POST request
    
#     queryset = CycleOnRoad.objects.filter(card=request.user.profile.card)
#     serializer_class = RideSerializer
@csrf_exempt
def RideHistory(request):
    username=request.POST.get("username")
    password=request.POST.get("password")
    user=authenticate(request,username=username,password=password)
    if user:
        queryset = CycleOnRoad.objects.filter(card=user.profile.card)
        
        cycle_history= RideSerializer(queryset,many=True)
        return JsonResponse({"history":cycle_history.data},status=200)
    else:
        return HttpResponse(status=400)
@csrf_exempt
def ChangePassword(request):
    username=request.POST.get("username")
    password=request.POST.get("password")
    user=authenticate(request,username=username,password=password)
    if user:
        new_password=request.POST.get("new_password")
        old_password_given=request.POST.get("old_password")
        old_password=user.password
        checking_user=authenticate(request,username=username,password=old_password_given)
        if checking_user == None:
            return JsonResponse({"message":"Incorrect Password"},status=400)
        user.set_password(new_password)
        if old_password == user.password:
            return JsonResponse({"message":"same as old password"},status=400)
        else:
            user.save()
        return JsonResponse({"message":"Password changed successfully"},status=200)
    else:
        return HttpResponse(status=400)
@csrf_exempt
def EndRide(request):
    username=request.POST.get("username")
    password=request.POST.get("password")
    user=authenticate(request,username=username,password=password)
    if user:
        card=request.POST.get("card")
        card=Card.objects.get(pk=int(card))
        initial_time= time.time()
        global current_rider_for_end
        current_rider_for_end=Rider(user.username,initial_time)
        
        return JsonResponse({"message":'Timer Initiated'},status=200)
    else:
        return HttpResponse(status=400)

@csrf_exempt
def complain(request):
    username=request.POST.get("username")
    password=request.POST.get("password")
    user=authenticate(request,username=username,password=password)
    if user:
        complain_text= request.POST.get("complain_text")
        cycle_number= request.POST.get("cycle_num")
        cycle_location= request.POST.get("cycle_loc")
        cycle= Cycle.objects.get(no=int(cycle_number))
        complaint= Complain.objects.create(
            user=user,
            cycle=cycle,
            loc_cycle=cycle_location,
            complain= complain_text
        )
        return JsonResponse({"message":"Complain Submitted"},status=201)
    else:
        return HttpResponse(status=400)

@csrf_exempt
def feedback(request):
    username=request.POST.get("username")
    password=request.POST.get("password")
    user=authenticate(request,username=username,password=password)
    if user:
        feedback_text= request.POST.get("feedback_text")
        feedback_submitted= Feedback.objects.create(
            user=user,
            feedback=feedback_text
        )
        return JsonResponse({"message":"Feedback Submitted"},status=201)
    else:
        return HttpResponse(status=400)
@csrf_exempt    
def EditProfile(request):
    username=request.POST.get("username")
    password=request.POST.get("password")
    user=authenticate(request,username=username,password=password)
    if user:
        full_name= request.POST.get("fullname")
        
        if name_validator(full_name) == False:
            return JsonResponse({"message":"Invalid name"},status=400)
        email=request.POST.get("email")
        if email_validator(email) == False:
            return JsonResponse({"message":"Invalid email"},status=400)
        contact=request.POST.get("phone")
        if phone_validator(contact) == False:
            return JsonResponse({"message":"Invalid phone number"},status=400)
        full_name= full_name.split(" ")
        if len(full_name) <=2:
            first_name=full_name[0]
            last_name=full_name[1]
        else:
            first_name=''
            for i in range(len(full_name)-2):
                first_name+=f"{full_name[i]} "
            last_name= full_name[-1]    
        user.first_name=first_name
        user.last_name=last_name
        user.email=email
        user.profile.phone=contact
        user.save()
        user.profile.save()
        return JsonResponse({"message":"Profile edited successfully"},status=200)
    
@csrf_exempt
def AccountDetails(request,username):
    user=User.objects.get(username=username).profile
    profile_serialized= ProfileSerializer(user).data
    return JsonResponse({"user":profile_serialized},status=200)
    
