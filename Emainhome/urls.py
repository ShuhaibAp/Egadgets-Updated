from django.urls import path
from .views import *

urlpatterns=[
    path('',HomePage.as_view(),name='home'),
    path('pdetailslink/<str:cat>',ProductListLink.as_view(),name='plink'),
    path('pdet/<int:id>',ProductDetails.as_view(),name='pdet'),
    path('cprod/<int:id>/',CartAdd,name='cprod'),
    path('clist/',CartList.as_view(),name='clist'),
]