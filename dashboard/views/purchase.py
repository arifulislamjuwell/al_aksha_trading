from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from dashboard.models import Area, Commission, Customer, MyDeposite, MyTransaction, OpcPurchase, PccPurchase, Purchase, Sell
from django.contrib.auth.models import User
import logging
from django.db.models import Q

logger = logging.getLogger('tutul_traders')

class PurchaseView(View):

    def get(self, request):
        data= request.GET

        purchase= Purchase.objects.all().order_by('-id')
        context={
             'purchase': purchase,
        }
        return render(request, 'purchase.html', context)

    
class CreatePurchaseView(View):

    def get(self, request):
        return render(request, 'create_purchase.html')

    def post(self,  request):
        data= request.POST
        purchase_type_list= []
        
        sub_total= data.get('sub_total')
        paid=data.get('paid')
        if data.get('opc_check'):
            opc_quantity= data.get('opc_quantity')
            opc_unit_price= data.get('opc_unit_price')
            opc_total= data.get('opc_total')
            purchase_type_list.append(1)

        if data.get('pcc_check'):
            pcc_quantity= data.get('pcc_quantity')
            pcc_unit_price= data.get('pcc_unit_price')
            pcc_total= data.get('pcc_total')
            purchase_type_list.append(2)

        purchase= Purchase()
        purchase.sub_total= int(sub_total)
        purchase.paid= int(paid)
        purchase.cement_type= ','.join([str(elem) for elem in purchase_type_list])
        purchase.save()

        if data.get('opc_check'):
            opc= OpcPurchase()
            opc.purchase= purchase
            opc.quantity= int(opc_quantity)
            opc.unit_price= float(opc_unit_price)
            opc.total= int(opc_total)
            opc.save()
        
        if data.get('pcc_check'):
            pcc= PccPurchase()
            pcc.purchase= purchase
            pcc.quantity= int(pcc_quantity)
            pcc.unit_price= float(pcc_unit_price)
            pcc.total= int(pcc_total)
            pcc.save()

        return redirect('dashboard:purchase_url')

class CommissionView(View):

    def get(self, request):
        data= request.GET
        name= data.get('area')
        commission= Commission.objects.all()
        if name:
            area= area.filter(name__icontains= name)
        context={
            'commission': commission
        }
        return render( request, 'commission.html', context)

    def post(self, request):
        data= request.POST
        total= data.get('total')
        date= data.get('date')
        unit=  data.get('unit')
        exist= Commission.objects.filter(date__month= date.split('-')[1])
        if exist.exists():
            return redirect('dashboard:commission_url')
        else:
            commission_obj=  Commission()
            commission_obj.date= date
        commission_obj.amount= int(total)
        commission_obj.unit_amount= float(unit)
        commission_obj.save()
        return redirect('dashboard:commission_url')


class MyTransactionView(View):

    def get(self, request):
        my_transaction= MyTransaction.objects.all().order_by('-id')

        context= {
            'my_transaction': my_transaction
        }
        return render(request, 'my_transaction.html', context)



class MyDepositeView(View):

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
        depo = MyDeposite()
        depo.amount= amount
        depo.save()

        return redirect('dashboard:my_deposite_url')