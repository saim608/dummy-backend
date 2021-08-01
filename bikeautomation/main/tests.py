from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile
from django.http import HttpResponse,JsonResponse
from .validators import email_validator,name_validator,phone_validator,nic_validator
# Create your tests here.
class InitialTest(TestCase):
    def Setup(self):
         self.user = User.objects.create_user(first_name="Syed Bilal", last_name="Ali", email="syed.bil.sba@gmail.com",
                                        username='syedbilal28', password='hellojee')
    def test1(self):
        full_name= "Syed Bilal Ali"
        if name_validator(full_name) == False:
            return JsonResponse({"message":"Invalid name"},status=400)
        email="syed.bilal.sba@gmail.com"
        if email_validator(email) == False:
            return JsonResponse({"message":"Invalid email"},status=400)

        username="bilal"
        contact="03428178566"
        if phone_validator(contact) == False:
            return JsonResponse({"message":"Invalid phone number"},status=400)
        password="password"
        nic="42101-6008811-5"
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
        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=password,

        )
        profile=Profile.objects.create(
            user=user,
            nic=nic,
            phone=contact
        )
