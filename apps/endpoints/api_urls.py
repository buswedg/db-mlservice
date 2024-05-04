from django.urls import path

from apps.endpoints.api_views import MLAlgorithmAPIView, MLAlgorithmStatusAPIView, MLAlgorithmRequestAPIView, \
    PredictAPIView, StartABTestAPIView, StopABTestAPIView, EndpointAPIView

app_name = "endpoints"

urlpatterns = [

    path('endpoint/', EndpointAPIView.as_view(), name='endpoint'),
    path('ml-algorithm/', MLAlgorithmAPIView.as_view(), name='ml_algorithm'),
    path('ml-algorithm-request/', MLAlgorithmRequestAPIView.as_view(), name='ml_algorithm_request'),
    path('ml-algorithm-status/', MLAlgorithmStatusAPIView.as_view(), name='ml_algorithm_status'),
    path('predict/<str:endpoint_name>/', PredictAPIView.as_view(), name='predict'),
    path('start_ab/', StartABTestAPIView.as_view(), name='start_ab'),
    path('stop_ab/<int:ab_test_id>/', StopABTestAPIView.as_view(), name='stop_ab'),

]
