from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from dashboard.models import BUY, COMMISSION,DEPOSITE, Area, Commission, Customer, MyDeposite, MyTransaction, OpeningInformation, Purchase, Sell, MINUS
from django.contrib.auth.models import User
import logging
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.transaction import my_transasction_dict_make


logger = logging.getLogger('tutul_traders')

class PurchaseView(LoginRequiredMixin, View):

    def get(self, request):
        data= request.GET
        id= data.get('id')
        cement_search= data.get('type')
        purchase= Purchase.objects.all().order_by('-id')
        
        if id:
            purchase = purchase.filter(id = id)
        if cement_search:
            purchase = purchase.filter(cement_type = cement_search)

        context={
             'purchase': purchase,
        }
        return render(request, 'purchase/purchase.html', context)

    
class CreatePurchaseView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'purchase/create_purchase.html')

    def post(self,  request):
        data= request.POST  
        cement_type= data.get('cement_type')
    
        quantity= data.get('quantity')
        unit_price= data.get('unit_price')
        total= data.get('total')
        date= data.get('date')

        purchase= Purchase()
        purchase.sub_total= int(total)
        purchase.cement_type= int(cement_type)
        purchase.unit_price= float(unit_price)
        purchase.quantity= int(quantity)
        purchase.created_at = date
        purchase.save()

        return redirect('dashboard:purchase_url')

class CommissionView(LoginRequiredMixin, View):

    def get(self, request):
        data= request.GET
        name= data.get('area')
        commission= Commission.objects.all().order_by('-id')
        if name:
            commission= commission.filter(name__icontains= name)
        context={
            'commission': commission
        }
        return render( request, 'commission.html', context)

    def post(self, request):
        data= request.POST
        total= data.get('total')
        date= data.get('date')
        unit=  data.get('unit')
        note=  data.get('note')

        # exist= Commission.objects.filter(date__month= date.split('-')[1])
        # if exist.exists():
        #     return redirect('dashboard:commission_url')
        # else:
        commission_obj=  Commission()
        commission_obj.date= date
        commission_obj.amount= int(total)
        commission_obj.unit_amount= float(unit)
        commission_obj.note= note
        commission_obj.save()
        return redirect('dashboard:commission_url')


class UpdateCommissionView(View):

    def get(self, request, id= None):
        commission= Commission.objects.get(id= id)
        context={
            'commission': commission
        }
        return render( request, 'update_commission.html', context)

    def post(self, request):
        data= request.POST
        total= data.get('total')
        date= data.get('date')
        unit=  data.get('unit')
        note=  data.get('note')

        # exist= Commission.objects.filter(date__month= date.split('-')[1])
        # if exist.exists():
        #     return redirect('dashboard:commission_url')
        # else:
        commission_obj=  Commission()
        commission_obj.date= date
        commission_obj.amount= int(total)
        commission_obj.unit_amount= float(unit)
        commission_obj.note= note
        commission_obj.save()
        return redirect('dashboard:commission_url')



class MyTransactionView(LoginRequiredMixin, View):

    def get(self, request):
        data= request.GET
        opening_balance = 0
        opening_information = OpeningInformation.objects.first()
        if opening_information:
            opening_balance = -opening_information.my_balance if opening_information.my_balance_type == MINUS else opening_information.my_balance
        current_balance = opening_balance
        
        transactions= MyTransaction.objects.all()
        row_list = my_transasction_dict_make(transactions, current_balance)
            
        context={
            'row_list': row_list,
            'opening_balance': opening_balance
          
        }
        return render(request, 'my_transaction.html', context)



class UpdatePurchaseView(View):

    def get(self, request, id):
        purchase = Purchase.objects.get(id= id)
        return render(request, 'purchase/update_purchase.html', {'purchase': purchase})

    def post(self,  request, id):
        data= request.POST  
        cement_type= data.get('cement_type')
        quantity= data.get('quantity')
        unit_price= data.get('unit_price')
        total= data.get('total')
        date= data.get('date')

        purchase= Purchase.objects.get(id= id)
        purchase.sub_total= int(total)
        purchase.cement_type= int(cement_type)
        purchase.unit_price= float(unit_price)
        purchase.quantity= int(quantity)
        purchase.created_at = date
        purchase.save()

        return redirect('dashboard:purchase_url')