from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from dashboard.models import Area, Customer, CustomerTransaction, CustomerDeposit, OPC, Sell, BUY, CASH
from django.contrib.auth.models import User
import logging
from django.db.models import Q
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin

logger = logging.getLogger('tutul_traders')

class SellView(LoginRequiredMixin, View):

    def get(self, request):
        data= request.GET
        customer_search= data.get('customer')
        area_search= data.get('area')
        cement_search= data.get('type')
        range= data.get('range')
        id= data.get('id')
        
        customer= Customer.objects.all().order_by('-id')
        sell= Sell.objects.all().order_by('-id')
        area= Area.objects.all().order_by('-id')

        if id:
            sell= sell.filter(id= id)

        if cement_search:
            sell= sell.filter(cement_type= cement_search)
        if customer_search:
             sell= sell.filter(
                 Q(customer__name__icontains= customer_search) |
                 Q(customer__phone_number__icontains= customer_search)
             )
        if area_search:
            sell= sell.filter(customer__area__id= area_search)

        if range:
            start, end = range.split(' - ')[0], range.split(' - ')[1]
            sell= sell.filter(created_at__range= [start, end])


        total_data= sell.aggregate(total_quantity=Sum('quantity'), bill=Sum('total_bill'), total_paid=Sum('paid_amount'))
    
        context={
            'customer': customer,
            'area': area,
            'sell': sell,
            'total_data': total_data
        }
        return render(request, 'sell/sell_list.html', context)

    
class CreateSellView(LoginRequiredMixin , View):

    def get(self, request):
        customer= Customer.objects.values('id', 'name', 'phone_number').order_by('name')

        context ={
            'customer': customer
        }
        return render(request, 'sell/create_sell.html', context)

    def post(self,  request):
        data= request.POST
        customer= data.get('customer')
        quantity= data.get('quantity')
        type_= data.get('type')
        unit_price= data.get('unit_price')
        total=  data.get('total')
        date=  data.get('date')
        paid=  data.get('paid')

        sell= Sell()
        sell.paid_amount= int(paid)
        sell.customer_id= customer
        sell.cement_type= int(type_)
        sell.quantity= int(quantity)
        sell.total_bill = int(total)
        sell.unit_price =  float(unit_price)
        sell.balance_sector = CASH
        sell.created_at = date
        sell.save()
        return redirect('dashboard:sell_url')


class UpdateSellView(View):

    def get(self, request, id=None):
        customer= Customer.objects.values('id', 'name', 'phone_number').order_by('name')
        sell = Sell.objects.get(id = id)

        context ={
            'customer': customer,
            'sell': sell
        }
        return render(request, 'sell/update_sell.html', context)


    def post(self,  request, id):
        data= request.POST
        customer= data.get('customer')
        quantity= data.get('quantity')
        type_= data.get('type')
        unit_price= data.get('unit_price')
        total=  data.get('total')
        date=  data.get('date')
        paid=  data.get('paid')

        sell= Sell.objects.get(id= id)
        sell.paid_amount= int(paid)
        sell.customer_id= customer
        sell.cement_type= int(type_)
        sell.quantity= int(quantity)
        sell.total_bill = int(total)
        sell.unit_price =  float(unit_price)
        sell.created_at = date
        sell.save()
        return redirect('dashboard:sell_url')