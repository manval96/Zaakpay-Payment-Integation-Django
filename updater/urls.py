from django.urls import path
from . import views

urlpatterns = [
    path('update_server', views.update, name='update'),
]