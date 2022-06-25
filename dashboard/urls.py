
from django.contrib import admin
from django.urls import path, include

from dashboard.views.dashboard import DashboardView, RevenueView, GenerateRevenueView, RemoveView, OpeningInfoView ,AccountView
from dashboard.views.customer import CustomerView
from dashboard.views.area import AreaView
from dashboard.views.sell import SellView, CreateSellView, UpdateSellView
from dashboard.views.deposite import BankDepositView, DepositView, MyDepositView, TransactionView, UpdateBankDepositView, UpdateCustomerDepositView, UpdateMyDepositView
from dashboard.views.purchase import PurchaseView, CreatePurchaseView, CommissionView, MyTransactionView, UpdatePurchaseView, UpdateCommissionView
from dashboard.views.download_view import DownloadView

app_name= 'dashboard'

urlpatterns = [
    path('', DashboardView.as_view(), name="dashboard_url"),

    path('opening-info/', OpeningInfoView.as_view(), name="opening_info_url"),


    path('area/', AreaView.as_view(), name="area_url"),
    
    path('customer/', CustomerView.as_view(), name="customer_url"),
    path('update-customer/<int:id>/', CustomerView.as_view(), name="update_customer_url"),
    path('customer-deposit/', DepositView.as_view(), name="deposite_url"),
    path('update-customer-deposit/<int:id>/', UpdateCustomerDepositView.as_view(), name="update_customer_deposit_url"),
    path('customer-transaction/<int:id>/', TransactionView.as_view(), name="transaction_url"),


    path('my-deposit/', MyDepositView.as_view(), name="my_deposite_url"),
    path('update-my-deposit/<int:id>/', UpdateMyDepositView.as_view(), name="update_my_deposit_url"),


    path('sell/', SellView.as_view(), name="sell_url"),
    path('create-sell/', CreateSellView.as_view(), name="create_sell_url"),
    path('update-sell/<int:id>/', UpdateSellView.as_view(), name="update_sell_url"),


    
    path('purchase/', PurchaseView.as_view(), name="purchase_url"),
    path('create-purchase/', CreatePurchaseView.as_view(), name="create_purchase_url"),
    path('update-purchase/<int:id>/', UpdatePurchaseView.as_view(), name="update_purchase_url"),


    path('commission/', CommissionView.as_view(), name="commission_url"),
    path('update-commission/<int:id>/', UpdateCommissionView.as_view(), name="update_commission_url"),

    path('my-transaction/', MyTransactionView.as_view(), name="my_transaction_url"),

    path('revenue/', RevenueView.as_view(), name="revenue_url"),
    path('generate-revenue/', GenerateRevenueView.as_view(), name="generate_revenue_url"),


    path('remove/', RemoveView.as_view(), name="remove_url"),

    path('download/', DownloadView.as_view(), name="download_url"),

    path('bank-deposit/', BankDepositView.as_view(), name="bank_deposit_url"),
    path('update-bank-deposit/<int:id>/', UpdateBankDepositView.as_view(), name="update_bank_deposit_url"),

    path('account/', AccountView.as_view(), name="account_url"),


]


