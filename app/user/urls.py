from django.urls import path
from user import views

from core import models

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create' ),
]
