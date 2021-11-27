from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from dashboard.models import Area, Customer, Sell
from django.contrib.auth.models import User
import logging
from django.db.models import Q

logger = logging.getLogger('tutul_traders')

class SellView(View):

    def get(self, request):
        data= request.GET
        customer_search= data.get('customer')
        area_search= data.get('area')
        cement_search= data.get('type')

        customer= Customer.objects.all()
        sell= Sell.objects.all()
        area= Area.objects.all()

        if cement_search:
            sell= sell.filter(cement_type= cement_search)
        if customer_search:
             sell= sell.filter(
                 Q(customer__name__icontains= customer_search) |
                 Q(customer__phone_number__icontains= customer_search)
             )
        if area_search:
            sell= sell.filter(customer__area__id= area_search)

        context={
            'customer': customer,
            'area': area,
            'sell': sell
        }
        return render(request, 'sell_list.html', context)

    
class CreateSellView(View):

    def get(self, request):
        customer= Customer.objects.all()

        context ={
            'customer': customer
        }
        return render(request, 'create_sell.html', context)

    def post(self,  request):
        data= request.POST
        customer= data.get('customer')
        quantity= data.get('quantity')
        address= data.get('address')
        type_= data.get('type')
        unit_price= data.get('unit_price')
        total=  data.get('total')
        paid=  data.get('paid')
        print(data)

        sell= Sell()
        sell.paid_amount= int(paid)
        sell.customer_id= customer
        sell.cement_type= type_
        if address:
            sell.delivery_address= address
        sell.quantity= int(quantity)
        sell.total_bill = int(total)
        sell.unit_price =  float(unit_price)
        sell.save()

        return redirect('dashboard:sell_url')