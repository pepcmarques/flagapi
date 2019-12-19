from django.urls import path
from flagapi.rest import views

app_name = 'rest'

urlpatterns = [
    path('simple/', views.SimpleClassificationApi.as_view(), name='simple_classification'),
    path('ml/', views.MachineLearningClassificationApi.as_view(), name='machine_classification'),
]
