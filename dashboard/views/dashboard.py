from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
import logging

class DashboardView(View):

    def get(self, request):
        return render(request, 'dashboard.html')