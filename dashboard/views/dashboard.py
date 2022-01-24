from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
import logging
from dashboard.models import Commission, Customer, Revenue, Sell, Stock, OPC, PCC
from django.db.models import Sum
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardView(LoginRequiredMixin, View):

    def get(self, request):
        stock= Stock.objects.first()
        return render(request, 'dashboard.html', {'stock': stock}) 

class RevenueView(LoginRequiredMixin, View):

    def get(self, request):
        customer= Customer.objects.all().order_by('-id')
        revenue= Revenue.objects.all().order_by('-id')
        return render(request, 'revenue.html',{'revenue': revenue, 'customer': customer})

class GenerateRevenueView(LoginRequiredMixin, View):
    def post(self, request):
        month_data= request.POST.get('month')
        pcc= request.POST.get('pcc')
        opc= request.POST.get('opc')

        month, year= month_data.split('-')[1], month_data.split('-')[0]

        sell= Sell.objects.all()
        for i in Customer.objects.all():
            cus_rev= Revenue.objects.filter(customer= i, date__month= month, date__year= year)
            if cus_rev:
                rev_object= cus_rev.first()
            else:
                rev_object= Revenue()
            customer_sell= sell.filter(created_at__month=  month, created_at__year= year, customer= i)
            rev_object.customer= i
            rev_object.date=  datetime.strptime(month_data+ '-30', "%Y-%m-%d").date()
            revenue= 0
            if customer_sell.exists():
                pcc_sell= customer_sell.filter(cement_type= PCC)
                if pcc_sell.exists():
                    pcc_value= pcc_sell.aggregate(total_quantity=Sum('quantity'), total_bill= Sum('total_bill'))
                    pcc_total_quantity= pcc_value.get('total_quantity')
                    pcc_total_bill= pcc_value.get('total_bill')
                    print(i.name, pcc_total_bill, pcc_total_quantity )

                    rev_object.pcc_sell= pcc_total_bill
                    rev_object.pcc_purchase= int(pcc) * pcc_total_quantity
                    revenue+= pcc_total_bill - (int(pcc) * pcc_total_quantity)
                   
                opc_sell= customer_sell.filter(cement_type= OPC)
                if opc_sell.exists():
                    opc_value=opc_sell.aggregate(total_quantity=Sum('quantity'), total_bill= Sum('total_bill'))
                    print(opc_value, i.name, 'opcccccc')
                    opc_total_quantity= opc_value.get('total_quantity')
                    opc_total_bill= opc_value.get('total_bill')

                    rev_object.opc_sell= opc_total_bill
                    rev_object.opc_purchase= int(opc) * opc_total_quantity
                    revenue+= opc_total_bill - (int(opc) * opc_total_quantity)
    
                rev_object.revenue= revenue
                rev_object.save()
            else:
                rev_object.save()
        return redirect('dashboard:revenue_url')
