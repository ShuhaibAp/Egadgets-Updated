from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView,FormView
from django.contrib.auth import authenticate,login,logout
from .forms import *
# Create your views here.

class loginview(FormView):
    template_name="login.html"
    form_class=EgLoginForm
    
    def post(self,request):
        form_data=EgLoginForm(data=request.POST)
        if form_data.is_valid():
            uname=form_data.cleaned_data.get('username')
            pswd=form_data.cleaned_data.get('password')
            user=authenticate(request,username=uname,password=pswd)
            login(request,user)
            if user:
                next_url = request.POST.get('next','/')
                return redirect(next_url)
            else:
                messages.error(request,"Invalid Username or Password")
                return render(request,"login.html",{'form':form_data})
        return render(request,"login.html",{'form':form_data})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', '/')
        return context

def logoutView(request):
    logout(request)
    next_url = request.GET.get('next','/')
    return redirect(next_url)