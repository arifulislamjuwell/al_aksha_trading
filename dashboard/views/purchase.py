from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from dashboard.models import Area, Customer, OpcPurchase, PccPurchase, Purchase, Sell
from django.contrib.auth.models import User
import logging
from django.db.models import Q

logger = logging.getLogger('tutul_traders')

class PurchaseView(View):

    def get(self, request):
        data= request.GET

        purchase= Purchase.objects.all()
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
        purchase.sub_total= sub_total
        purchase.paid= paid
        purchase.cement_type= ','.join([str(elem) for elem in purchase_type_list])
        purchase.save()

        if data.get('opc_check'):
            opc= OpcPurchase()
            opc.purchase= purchase
            opc.quantity= opc_quantity
            opc.unit_price= opc_unit_price
            opc.total= opc_total
            opc.save()
        
        if data.get('pcc_check'):
            pcc= PccPurchase()
            pcc.purchase= purchase
            pcc.quantity= pcc_quantity
            pcc.unit_price= pcc_unit_price
            pcc.total= pcc_total
            pcc.save()

        return redirect('dashboard:purchase_url')

class CommissionView(View):

    def get(self, request):
        data= request.GET
        name= data.get('area')
        area= Commission.objects.all()
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