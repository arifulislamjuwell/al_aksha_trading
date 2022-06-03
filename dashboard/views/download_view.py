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
from utils.xlsx_generate_report import my_transaction_download

logger = logging.getLogger('tutul_traders')

class DownloadView(LoginRequiredMixin, View):

    def get(self, request):
        data = request.GET
        bdaymonth = data.get('bdaymonth')
        type_ = data.get('type_')
        if type_ == 'my_t':
            return my_transaction_download(bdaymonth)
        return render(request, 'download.html')