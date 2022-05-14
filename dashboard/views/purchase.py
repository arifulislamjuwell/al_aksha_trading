from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from dashboard.models import BUY, COMMISSION,DEPOSITE, Area, Commission, Customer, MyDeposite, MyTransaction, OpeningInformation, Purchase, Sell, MINUS
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
        row_list = []
        transactions= MyTransaction.objects.all().order_by('-id')
        for transaction in transactions:
            content_object = transaction.content_object
            dic ={'id': transaction.id }
            if transaction.transaction_type == BUY:
                sub_total = content_object.sub_total
                quantity = content_object.quantity
                dic['date'] = content_object.created_at
                dic['transaction_type'] = 'Purchase'
                dic['quantity'] = quantity
                dic['details'] = '{} BAGS-50KG({})'.format(quantity,content_object.get_cement_type_display())
                dic['total_bill'] = sub_total
                dic['paid'] = 0
                current_balance = current_balance - sub_total
                dic['current_balance'] = current_balance

            elif transaction.transaction_type == DEPOSITE:
                amount = content_object.amount
                dic['date'] = content_object.created_at
                dic['transaction_type'] = 'DEPOSIT'
                dic['quantity'] = ''
                dic['details'] = content_object.note
                dic['total_bill'] = ''
                dic['paid'] = amount
                current_balance = current_balance  + amount
                dic['current_balance'] = current_balance
            
            else:
                amount = content_object.amount
                dic['date'] = content_object.date
                dic['transaction_type'] = 'COMMISSION'
                dic['quantity'] = ''
                dic['details'] = content_object.note
                dic['total_bill'] = ''
                dic['paid'] = amount
                current_balance = current_balance  + amount
                dic['current_balance'] = current_balance 

            row_list.append(dic)
            
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