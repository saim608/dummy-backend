from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    nic=models.CharField(max_length=15,null=False)
    phone=models.CharField(max_length=11,null=False)
    balance=models.FloatField(default=0)
    # card=models.OneToOneField("Card", on_delete=models.CASCADE)
    card=models.OneToOneField("Card",null=True,blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)

class Complain(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    cycle =models.ForeignKey("Cycle", on_delete=models.CASCADE)
    loc_cycle = models.CharField(max_length=30)
    complain = models.CharField(max_length=100)

    def __str__(self):
        return str(self.complain)

class Feedback(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    feedback = models.CharField(max_length=100)

    def __str__(self):
        return str(self.feedback)





class Cycle(models.Model):
    no = models.IntegerField()
    name=models.CharField(max_length=30)
    manufacturing_date=models.DateField()
    status=models.CharField(max_length=30)

    def __str__(self):
        return str(self.no)

class Maintenance(models.Model):
    cycle=models.ForeignKey(Cycle,null=True,on_delete=models.SET_NULL)
    date=models.DateField(auto_now_add=True)
    p_cost=models.IntegerField()
    u_cost=models.IntegerField()

class Card(models.Model):
    card_no=models.CharField(max_length=255)

    def __str__(self):
        return self.card_no

class CycleOnRoad(models.Model):
    cycle=models.ForeignKey(Cycle,on_delete=models.CASCADE)
    card= models.ForeignKey(Card,null=True,on_delete=models.SET_NULL)
    
    status=models.IntegerField(default="0")
    starting_time=models.DateTimeField(auto_now_add=True)
    end_time=models.DateTimeField(null=True,blank=True)
    charge=models.FloatField(null=True,blank=True)
    difference=models.FloatField(null=True,blank=True)
# class Ride(models.Model):


