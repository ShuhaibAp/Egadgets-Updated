from accounts.models import *

def cart_count(request):
    if request.user.is_authenticated:
        pcount=Cart.objects.filter(user=request.user).count()
        return {"c_count":pcount}
    return {"c_count":0}

def review_count(request):
    prod=request.resolver_match.kwargs.get('id')
    rcount=0
    if prod:
        rcount=Reviews.objects.filter(product=prod).count()
    return {"r_count":rcount}
    