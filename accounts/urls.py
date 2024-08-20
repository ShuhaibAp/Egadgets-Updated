from django.urls import path
from .views import *
urlpatterns=[
    path('log',loginview.as_view(),name='log'),
    path('lout',logoutView,name='lout'),
]