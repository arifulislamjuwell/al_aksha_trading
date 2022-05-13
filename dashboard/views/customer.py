from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from dashboard.models import Area, Customer
from django.contrib.auth.models import User
import logging
from django.db.models import Q

logger = logging.getLogger('tutul_traders')
from django.contrib.auth.mixins import LoginRequiredMixin

class CustomerView(LoginRequiredMixin, View):

    def get(self, request, id= None):
        if request.resolver_match.url_name == 'customer_url':
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
            area= Area.objects.values('id', 'name')
            context={
                'customer': customer,
                'area': area
            }
            return render(request, 'customer_list.html', context)

        if request.resolver_match.url_name == 'update_customer_url':
            customer = Customer.objects.get(id= id)
            area= Area.objects.values('id', 'name')

            return render(request, 'update_customer.html', {'customer': customer, 'area': area})


    def post(self, request, id= None):
        data= request.POST
        name= data.get('name')
        area= data.get('area')
        address= data.get('address')
        email= data.get('email')
        phone_number= data.get('phone_number')
        op_balance_type= data.get('op_balance_type')
        opening_balance= data.get('opening_balance')
        if request.resolver_match.url_name == 'customer_url':
            customer= Customer()
        if request.resolver_match.url_name == 'update_customer_url':
            customer= Customer.objects.get(id=id)
        customer.opening_balance_type = op_balance_type
        customer.opening_balance = opening_balance
        customer.name = name
        if email:
            customer.email = email
        customer.phone_number = phone_number
        customer.address = address
        customer.area_id= area
        customer.save() 
        return redirect('dashboard:customer_url')