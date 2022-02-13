from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from dashboard.models import Area, Commission, Customer, MyDeposite, MyTransaction,Purchase, Sell
from django.contrib.auth.models import User
import logging
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

logger = logging.getLogger('tutul_traders')

class PurchaseView(LoginRequiredMixin, View):

    def get(self, request):
        data= request.GET

        purchase= Purchase.objects.all().order_by('-id')
        context={
             'purchase': purchase,
        }
        return render(request, 'purchase.html', context)

    
class CreatePurchaseView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'create_purchase.html')

    def post(self,  request):
        data= request.POST  
        cement_type= data.get('cement_type')
       

        quantity= data.get('quantity')
        unit_price= data.get('unit_price')
        total= data.get('total')
        date= data.get('date')

        purchase= Purchase()
        purchase.sub_total= int(total)
        purchase.paid= 0
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
        print(data,'-------------------------------')
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
        my_transaction= MyTransaction.objects.order_by('-id')

        context= {
            'my_transaction': my_transaction
        }
        return render(request, 'my_transaction.html', context)



class MyDepositeView(LoginRequiredMixin, View):

    def get(self, request):
        data= request.GET
        deposite= MyDeposite.objects.all().order_by('-id')
        context={
            'deposite': deposite
        }
        return render( request, 'my_deposite.html', context)

    def post(self, request):
        data= request.POST
        amount= data.get('amount')
        note= data.get('note')
        date= data.get('date')

        depo = MyDeposite()
        depo.amount= amount
        depo.created_at = date
        if note:
            depo.note= note
        depo.save()

        return redirect('dashboard:my_deposite_url')