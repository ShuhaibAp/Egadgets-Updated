from django.urls import path
from .views import *

urlpatterns=[
    path('',HomePage.as_view(),name='home'),
    path('pdetailslink/<str:cat>',ProductListLink.as_view(),name='plink'),
    path('pdet/<int:id>',ProductDetails.as_view(),name='pdet'),
    path('cprod/<int:id>/',CartAdd,name='cprod'),
    path('clist/',CartList.as_view(),name='clist'),
    path('revadd/<int:id>',AddReview,name='revadd'),
    path('inc/<int:id>',IncQuantity,name='incQ'),
    path('decQ/<int:id>',DecQuantity,name='decQ'),
    path('RemC/<int:id>',RemoveCart,name='remC'),
    path('Chk/<int:id>',CheckOut.as_view(),name='chk'),
    path('Olist/',OrderList.as_view(),name='olist'),
    path('wadd/<int:id>',AddWish,name='wadd'),
    path('wlist/',WishList.as_view(),name='wlist'),
    path('wdel/<int:id>',RemoveWish,name='wdel'),
    path('odel/<int:id>',RemoveOrder,name='odel'),
]