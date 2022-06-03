from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
import logging
from dashboard.models import Area
from django.contrib.auth.mixins import LoginRequiredMixin
logger = logging.getLogger('tutul_traders')

class AreaView(LoginRequiredMixin, View):

    def get(self, request):
        data= request.GET
        name= data.get('area')
        area= Area.objects.all()
        if name:
            area= area.filter(name__icontains= name)
        context={
            'area': area
        }
        return render( request, 'area.html', context)

    def post(self, request):
        data= request.POST
        name= data.get('name')
        Area.objects.create(name= name)
        return redirect('dashboard:area_url')