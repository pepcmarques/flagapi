from django.urls import path
from flagapi.rest import views

urlpatterns = [
    path('', views.FirstApi.as_view(), name='first'),
]
