from django.urls import path
from .views import *
urlpatterns=[
    path('log',LoginView.as_view(),name='log'),
    path('lout',logoutView,name='lout'),
    path('reg',RegView.as_view(),name='reg'),
]