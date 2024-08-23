from accounts.models import *

def cart_count(request):
    if request.user.is_authenticated:
        product_count=Cart.objects.filter(user=request.user).count()
        return {"c_count":product_count}
    return {"c_count":0}

def review_count(request):
    prod=request.resolver_match.kwargs.get('id')
    rcount=0
    if prod:
        rcount=Reviews.objects.filter(product=prod).count()
    return {"r_count":rcount}

def order_count(request):
    if request.user.is_authenticated:
        order_count=Orders.objects.filter(user=request.user).count()
        return {"o_count":order_count}
    return {"o_count":0}