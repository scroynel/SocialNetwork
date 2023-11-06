from django.urls import path

from . import api

urlpatterns = [
    path('', api.notification, name='notifications'),
    path('read/<uuid:pk>/', api.read_notification, name='read_notification'),
]