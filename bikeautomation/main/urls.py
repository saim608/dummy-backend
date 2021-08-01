from django.urls import path,re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib.auth import views as auth_views
urlpatterns=[
    path('profile/',views.ProfileList.as_view()),
    path('profile/<int:pk>/',views.ProfileDetails.as_view()),
    path("signup/",views.signup,name="signup"),
    path("login/",views.Login,name="login"),
    path("ridenow/",views.RideNow,name="Ridenow"),
    path("verify/<str:card_num>/",views.Verifycard,name="verify"),
    path("ridehistory/",views.RideHistory,name="history"),
    path("changepassword/",views.ChangePassword,name="ChangePassword"),
    path("endride/",views.EndRide,name="EndRide"),
    path("complain/",views.complain,name="complain"),
    path("feedback/",views.feedback,name="feedback"),
    path("edit-profile/",views.EditProfile,name="EditProfile"),
    path("account/<str:username>/",views.AccountDetails,name="account"),
    path("getridestatus/",views.GetRideStatus,name="GetRideStatus"),
    path('forgetpassword/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'),
    
     name='password_reset'),
     path('password-reset-confirm/<uidb64>/<token>/',     auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
    name='password_reset_confirm'),
    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
     name='password_reset_done'),
     path('password-reset-complete/',
auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
     name='password_reset_complete'),
]

urlpatterns = format_suffix_patterns(urlpatterns)