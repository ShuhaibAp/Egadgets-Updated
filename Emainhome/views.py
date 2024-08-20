from django.shortcuts import render,redirect
from django.views.generic import TemplateView,ListView,DetailView,CreateView
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
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        current_product=self.get_object()
        context['relProducts']=Product.objects.filter(category=current_product.category).exclude(id=current_product.id)
        return context

def CartAdd(request,*args,**kwargs):
    pid=kwargs.get('id')
    prod=Product.objects.get(id=pid)
    if not request.user.is_authenticated:
        return redirect('log')
    user=request.user
    quant=request.POST.get('qty')
    try:
        cart=Cart.objects.get(product=prod,user=user)
        cart.quantity+=int(quant)
        cart.save()
        return redirect('pdet', id=pid)
    except:
        cart=Cart.objects.create(product=prod,user=user,quantity=quant)
        return redirect('pdet', id=pid)

class CartList(ListView):
    template_name="cartlist.html"
    queryset=Cart.objects.all()
    context_object_name='cart'
    def get_quryset(self):
        list=super().get_queryset.filter(user=self.request.user)

