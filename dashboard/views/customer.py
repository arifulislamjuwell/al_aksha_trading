from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from dashboard.models import Area, Customer
from django.contrib.auth.models import User
import logging
from django.db.models import Q

logger = logging.getLogger('tutul_traders')

class CustomerView(View):

    def get(self, request):
        data= request.GET
        customer_search= data.get('customer')
        area_search= data.get('area')
        customer= Customer.objects.all().order_by('-id')
        if customer_search:
            customer= customer.filter(
                Q(name__icontains= customer_search) |
                Q(phone_number__icontains= customer_search)
            )
        if area_search:
            customer= customer.filter(area__id= area_search)
        area= Area.objects.all()
        context={
            'customer': customer,
            'area': area
        }
        return render(request, 'customer_list.html', context)

    def post(self, request):
        data= request.POST
        name= data.get('name')
        area= data.get('area')
        address= data.get('address')
        email= data.get('email')
        phone_number= data.get('phone_number')

        customer= Customer()
        customer.name = name
        if email:
            customer.email = email
        customer.phone_number = phone_number
        customer.address = address
        customer.area_id= area
        customer.save() 
        return redirect('dashboard:customer_url')