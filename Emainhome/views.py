from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.generic import TemplateView,ListView,DetailView,CreateView
from django.contrib import messages
from accounts.models import *
# Create your views here.
class HomePage(TemplateView):
    template_name="homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['newProducts'] = Product.objects.all()  # Fetch all products
        return context

class ProductListLink(ListView):
    template_name="productlist.html"
    queryset=Product.objects.all()
    context_object_name="products"
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
        context['relProducts']=Product.objects.filter(category=prod.category).exclude(id=prod.id)
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
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            request.session['next'] = request.get_full_path()
            return redirect('log')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

def IncQuantity(request,**kwargs):
    pid=kwargs.get('id')
    cart=Cart.objects.get(id=pid)
    cart.quantity+=1
    cart.save()
    return redirect('clist')

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

def RemoveCart(request,**kwargs):
    pid=kwargs.get('id')
    cart=Cart.objects.get(id=pid)
    cart.delete()
    return redirect('clist')

    
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

class OrderList(ListView):
    template_name="orderlist.html"
    queryset=Orders.objects.all()
    context_object_name='order'
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)