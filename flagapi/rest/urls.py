from django.urls import path
from flagapi.rest import views

app_name = 'rest'

urlpatterns = [
    path('include/', views.IncludeClassificationApi.as_view(), name='include_classification'),
    path('simple/', views.SimpleClassificationApi.as_view(), name='simple_classification'),
    path('ml/', views.MachineLearningClassificationApi.as_view(), name='machine_classification'),
]
