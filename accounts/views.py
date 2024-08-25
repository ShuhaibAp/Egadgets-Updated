from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView,CreateView,FormView
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .forms import *
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
# Create your views here.

class LoginView(FormView):
    template_name="login.html"
    form_class=EgLoginForm

    def post(self, request):
        form_data=EgLoginForm(data=request.POST)
        if form_data.is_valid():
            uname=form_data.cleaned_data.get('username')
            pswd=form_data.cleaned_data.get('password')
            user=authenticate(request, username=uname, password=pswd)
            if user is not None:
                login(request, user)
                next_url=request.POST.get('next',request.session.pop('next', '/'))
                return redirect(next_url)
            else:
                messages.error(request, "Invalid Username or Password")
        return render(request, "login.html", {'form': form_data})

    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', '/')
        return context

@never_cache
def logoutView(request):
    logout(request)
    next_url = request.GET.get('next','/')
    return redirect(next_url)

class RegView(CreateView):
    template_name="register.html"
    form_class=ERegForm
    success_url=reverse_lazy('log')

    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

