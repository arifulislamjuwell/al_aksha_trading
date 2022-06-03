from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
import logging

logger = logging.getLogger('tutul_traders')

class AuthenticationView(View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        if request.resolver_match.url_name == 'login_url':
            return render (request, 'login.html',{'page_title': 'Login'})

        if request.resolver_match.url_name == 'logout_url':
            auth.logout(request)
            return redirect('login_url')

    def post(self, request):
        if request.resolver_match.url_name == 'login_url':
            username= request.POST['username'].strip()
            password= request.POST['password'].strip()

            try:
                user= User.objects.get(username= username)
            except Exception as e:
                return render(request,'login.html',{'error':'This Number doesn\'t exist, please input your valid Number'})
            if user.check_password(password):
                user= auth.authenticate(username=user.username, password=password)
                if user is not None:
                    auth.login(request, user)
                    return redirect('dashboard:dashboard_url')
            else:
                return render(request,'login.html',{'error':'Password doesn\'t match '})