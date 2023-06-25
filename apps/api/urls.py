from django.urls import path, include
from rest_framework_simplejwt import views

app_name = "api"

urlpatterns = [

    path('token/', views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', views.TokenVerifyView.as_view(), name='token_verify'),
    path('token/blacklist/', views.TokenBlacklistView.as_view(), name='token_blacklist'),

    path('account/', include('apps.account.api_urls', namespace='account')),

    path('v1/', include('apps.endpoints.api_urls', namespace='endpoints')),

]
