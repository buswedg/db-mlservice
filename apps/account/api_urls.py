from django.urls import path

from apps.account import api_views

app_name = "account"

urlpatterns = [

    path('register/', api_views.RegistrationAPIView.as_view(), name='register'),
    path('login/', api_views.LoginAPIView.as_view(), name='login'),
    path('user/retrieve/', api_views.UserRetrieveUpdateAPIView.as_view(), name='user_retrieve'),
    path('user/update/', api_views.UserRetrieveUpdateAPIView.as_view(), name='user_update'),
    path('logout/', api_views.LogoutAPIView.as_view(), name='logout'),

]
