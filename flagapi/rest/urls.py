from django.urls import path
from flagapi.rest import views

app_name = 'rest'

urlpatterns = [
    path('', views.FirstApi.as_view(), name='first'),
]
