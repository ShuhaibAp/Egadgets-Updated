from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.generic import TemplateView,ListView,DetailView,CreateView
from django.contrib import messages
from accounts.models import *
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# Create your views here.
class HomePage(TemplateView):
    template_name="homepage.html"

    # @method_decorator(never_cache)
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['newProducts'] = Product.objects.all()
        return context

class ProductListLink(ListView):
    template_name="productlist.html"
    queryset=Product.objects.all()
    context_object_name="products"
    paginate_by=12

    def get_queryset(self):
        qset=super().get_queryset().filter(category=self.kwargs.get('cat'))
        return qset

class ProductDetails(DetailView):
    template_name="productdetails.html"
    queryset=Product.objects.all()
    context_object_name="product"
    pk_url_kwarg='id'

    def dispatch(self,request,*args,**kwargs):
        if 'pdet/' in request.path:
            return super().dispatch(request, *args, **kwargs)
        
        if not request.user.is_authenticated:
            request.session['next']=request.get_full_path()
            return redirect(reverse('log')+ '?next=' + request.get_full_path())
        return super().dispatch(request,*args,**kwargs)    

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        prod=self.get_object()
        #taking the reviews from table and passing to 'review' context.
        reviews=Reviews.objects.filter(product=prod)
        context['review']=reviews
        #taking the products from table based on category with ignoring current product and passing to 'relProducts' context.
        # context['relProducts']=Product.objects.filter(category=prod.category).exclude(id=prod.id)
        # return context
        relProducts = Product.objects.filter(category=prod.category).exclude(id=prod.id)
        # Implementing pagination for related products (10 products per page)
        paginator = Paginator(relProducts, 8)  # Show 10 related products per page
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        # Adding paginated related products to the context
        context['page_obj'] = page_obj
        return context


def CartAdd(request,*args,**kwargs):
    pid=kwargs.get('id')
    prod=Product.objects.get(id=pid)
    if not request.user.is_authenticated:
        request.session['next'] = request.get_full_path()
        return redirect(reverse('log') + '?next=' + request.get_full_path())
    user=request.user
    quant=request.POST.get('qty')
    try:
        cart=Cart.objects.get(product=prod,user=user)
        cart.quantity+=int(quant)
        cart.save()
    except:
        if not quant:
            return redirect(request.session.pop('next', 'pdet'), id=prod.id)
        cart=Cart.objects.create(product=prod,user=user,quantity=quant)
    next_url = request.session.pop('next', 'pdet')
    return redirect('pdet', id=pid)

class CartList(ListView):
    template_name="cartlist.html"
    queryset=Cart.objects.all()
    context_object_name='cart'
    
    # @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            request.session['next'] = request.get_full_path()
            return redirect('log')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

# @never_cache
def IncQuantity(request,**kwargs):
    pid=kwargs.get('id')
    cart=Cart.objects.get(id=pid)
    cart.quantity+=1
    cart.save()
    return redirect('clist')

# @never_cache
def DecQuantity(request,**kwargs):
    pid=kwargs.get('id')
    cart=Cart.objects.get(id=pid)
    if cart.quantity == 1:
        cart.delete()
        return redirect('clist')
    else:
        cart.quantity -= 1
        cart.save()
    return redirect('clist')

# @never_cache
def RemoveCart(request,**kwargs):
    pid=kwargs.get('id')
    cart=Cart.objects.get(id=pid)
    cart.delete()
    return redirect('clist')

# @never_cache
def AddReview(request,*args,**kwargs):
    pid=kwargs.get('id')
    prod=Product.objects.get(id=pid)
    if not request.user.is_authenticated:
        request.session['next'] = request.get_full_path()
        return redirect('log')  
    user=request.user
    rev=request.POST.get('user-review')
    if not rev:
        return redirect(request.session.pop('next', 'pdet'), id=prod.id)
    Reviews.objects.create(content=rev,user=user,product=prod)
    next_url = request.session.pop('next', 'pdet')
    return redirect ('pdet', id=prod.id)

class CheckOut(DetailView):
    template_name="checkout.html"
    queryset=Cart.objects.all()
    pk_url_kwarg="id"
    context_object_name='item'
    def post(self,request,*args,**kwargs):
        addr=request.POST.get('address')
        ph=request.POST.get('phone')
        pid=kwargs.get('id')
        cart=Cart.objects.get(id=pid)
        prod=cart.product
        quant=cart.quantity
        if not request.user.is_authenticated:
            request.session['next'] = request.get_full_path()
            return redirect('log')
        user=request.user
        Orders.objects.create(product=prod,user=user,quantity=quant,address=addr,phone=ph)
        cart.delete()
        return redirect('clist')

    # @method_decorator(never_cache)
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)

class OrderList(ListView):
    template_name="orderlist.html"
    queryset=Orders.objects.all()
    context_object_name='order'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            request.session['next'] = request.get_full_path()
            return redirect('log')
        return super().dispatch(request, *args, **kwargs)
    # @method_decorator(never_cache)
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

# @never_cache
def AddWish(request,*args,**kwargs):
    if not request.user.is_authenticated:
        request.session['next'] = request.get_full_path()
        return redirect('log')
    pid=kwargs.get('id')
    product=Product.objects.get(id=pid)
    product.wish.add(request.user)
    return redirect('home')

class WishList(ListView):
    template_name='wishlist.html'
    queryset=Product.objects.all()
    context_object_name='items'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            request.session['next'] = request.get_full_path()
            return redirect('log')
        return super().dispatch(request, *args, **kwargs)

    # @method_decorator(never_cache)
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(wish=self.request.user)

# @never_cache
def RemoveWish(request,*args,**kwargs):
    pid=kwargs.get('id')
    product=Product.objects.get(id=pid)
    product.wish.remove(request.user)
    return redirect('wlist')
 
def RemoveOrder(request,*args,**kwargs):
    pid=kwargs.get('id')
    product=Orders.objects.get(id=pid).delete()
    return redirect('olist')
 