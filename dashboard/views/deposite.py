from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
import logging
from dashboard.models import Area, Customer, CustomerTransaction, Deposite
from django.db.models import Q


logger = logging.getLogger('tutul_traders')

class DepositeView(View):

    def get(self, request):
        data= request.GET
        customer_search= data.get('customer')
        deposite= Deposite.objects.all().order_by('-id')
        customer= Customer.objects.all()
        if customer_search:
            deposite= deposite.filter(
                Q(customer__name__icontains= customer_search) |
                Q(customer__phone_number__icontains= customer_search)
            )

        context={
            'deposite': deposite,
            'customer': customer
        }
        return render( request, 'deposite.html', context)

    def post(self, request):
        data= request.POST
        customer= data.get('customer')
        amount= data.get('amount')

        depo = Deposite()
        depo.customer_id= customer
        depo.amount= amount
        depo.save()

        return redirect('dashboard:deposite_url')

    
class TransactionView(View):
    def get(self, request, id):
        data= request.GET

        transaction= CustomerTransaction.objects.filter(customer__id= id).order_by('-id')

        context={
            'transaction': transaction,
          
        }
        return render( request, 'transaction.html', context)