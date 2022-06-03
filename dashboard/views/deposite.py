from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
import logging
from dashboard.models import Area, Customer, CustomerTransaction, CustomerDeposit, MyDeposite, BUY, MINUS
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin


logger = logging.getLogger('tutul_traders')

class DepositView(LoginRequiredMixin, View):

    def get(self, request):
        data= request.GET
        customer_search= data.get('customer')
        deposite= CustomerDeposit.objects.all().order_by('-id')
        customer= Customer.objects.values('id', 'name', 'phone_number')
        if customer_search:
            deposite= deposite.filter(
                Q(customer__name__icontains= customer_search) |
                Q(customer__phone_number__icontains= customer_search)
            )

        context={
            'deposite': deposite,
            'customer': customer
        }
        return render( request, 'deposit/deposite.html', context)

    def post(self, request):
        data= request.POST
        customer= data.get('customer')
        amount= data.get('amount')
        date= data.get('date')
        note= data.get('note')

        depo = CustomerDeposit()
        depo.customer_id= customer
        depo.amount= amount
        depo.created_at = date
        depo.note = note
        depo.save()

        return redirect('dashboard:deposite_url')

    
class TransactionView(LoginRequiredMixin, View):
    def get(self, request, id):
        data= request.GET
        customer= Customer.objects.get(id= id)
        opening_balance = -customer.opening_balance if customer.opening_balance_type == MINUS else customer.opening_balance
        current_balance = opening_balance
        row_list = []
        transactions= CustomerTransaction.objects.filter(customer= customer)
        for transaction in transactions:
            content_object = transaction.content_object
            dic= {}
            dic ={'id': content_object.id }
            if transaction.transaction_type == BUY:
                total_bill = content_object.total_bill
                paid_amount =  content_object.paid_amount
                quantity = content_object.quantity
                dic['date'] = content_object.created_at
                dic['transaction_type'] = 'BUY'
                dic['quantity'] = quantity
                dic['details'] = '{} BAGS-50KG({})'.format(quantity,content_object.get_cement_type_display())
                dic['date'] = content_object.created_at
                dic['total_bill'] = total_bill
                dic['type_'] = 1
                dic['paid'] = content_object.paid_amount
                current_balance = (current_balance - total_bill) + paid_amount
                dic['current_balance'] = current_balance

            else:
                amount = content_object.amount
                dic['date'] = content_object.created_at
                dic['transaction_type'] = 'DEPOSITE'
                dic['quantity'] = ''
                dic['details'] = content_object.note
                dic['date'] = content_object.created_at
                dic['total_bill'] = ''
                dic['paid'] = amount
                dic['type_'] = 2
                current_balance = current_balance  + amount
                dic['current_balance'] = current_balance

            row_list.append(dic)


        print(row_list)
        context={
            'row_list': row_list,
            'customer': customer,
            'opening_balance': opening_balance
          
        }
        return render( request, 'transaction.html', context)


class UpdateCustomerDepositView(View):

    def get(self, request, id):
        deposit= CustomerDeposit.objects.get(id= id)
        customer= Customer.objects.values('id', 'name', 'phone_number')

        context={
            'deposit': deposit,
            'customer': customer
          
        }
        return render( request, 'deposit/update_customer_deposit.html', context)


    def post(self, request, id):
        data= request.POST
        customer= data.get('customer')
        amount= data.get('amount')
        date= data.get('date')
        note= data.get('note')

        depo = CustomerDeposit.objects.get(id = id)
        depo.customer_id= customer
        depo.amount= amount
        depo.note = note
        depo.created_at = date
        depo.save()

        return redirect('dashboard:deposite_url')


class MyDepositView(LoginRequiredMixin, View):

    def get(self, request):
        data= request.GET
        deposite= MyDeposite.objects.all().order_by('-id')
        context={
            'deposite': deposite
        }
        return render( request, 'deposit/my_deposite.html', context)

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


class UpdateMyDepositView(View):

    def get(self, request,id):
        deposit= MyDeposite.objects.get(id= id)
        context={
            'deposit': deposit
        }
        return render( request, 'deposit/update_my_deposite.html', context)

    def post(self, request, id):
        data= request.POST
        amount= data.get('amount')
        note= data.get('note')
        date= data.get('date')

        depo = MyDeposite.objects.get(id = id)
        depo.amount= amount
        depo.created_at = date
        if note:
            depo.note= note
        depo.save()

        return redirect('dashboard:my_deposite_url')