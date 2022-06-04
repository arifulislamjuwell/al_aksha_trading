from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
import logging
from dashboard.models import Area, BUY, Customer, CustomerDeposit, CustomerTransaction, MINUS, MyDeposite, MyTransaction
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.xlsx_generate_report import my_transaction_download, customer_transaction_download
from django.contrib import messages


logger = logging.getLogger('tutul_traders')

class DownloadView(LoginRequiredMixin, View):

    def get(self, request):
        data = request.GET
        bdaymonth = data.get('bdaymonth')
        type_ = data.get('type_')
        customer = data.get('customer')
        print(data)
        customers = Customer.objects.values('id', 'name', 'phone_number')
        if type_ == 'my_t':
            transactions= MyTransaction.objects.filter(created_at__year = bdaymonth.split('-')[0], created_at__month = bdaymonth.split('-')[1])
            if transactions.exists():
                return my_transaction_download(transactions)
            else:
                messages.error(request, 'Data Not Found!') 
                return redirect('dashboard:download_url')
        if type_ == 'cus_t':
            transactions= CustomerTransaction.objects.filter(customer_id= customer, created_at__year = bdaymonth.split('-')[0], created_at__month = bdaymonth.split('-')[1])
            if transactions.exists():
                return customer_transaction_download(transactions)
            else:
                messages.error(request, 'Data Not Found!') 
                return redirect('dashboard:download_url')
        return render(request, 'download.html', {'customers': customers})