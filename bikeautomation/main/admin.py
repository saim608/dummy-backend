from django.contrib import admin

from .models import Profile,Cycle,Maintenance,Card,CycleOnRoad,Complain,Feedback
# Register your models here.

admin.site.register(Profile)
admin.site.register(Cycle)
admin.site.register(Maintenance)
admin.site.register(Card)
class CycleOnRoadAdmin(admin.ModelAdmin):
    fields    = ('cycle', 'card','status','starting_time',"end_time","charge","difference")

    #list of fields to display in django admin
    list_display = ['id','cycle', 'card','status','starting_time',"end_time","charge","difference"]

admin.site.register(CycleOnRoad,CycleOnRoadAdmin)
admin.site.register(Complain)
admin.site.register(Feedback)



