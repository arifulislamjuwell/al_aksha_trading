
from django.contrib import admin
from django.urls import path, include

from dashboard.views.dashboard import DashboardView
from dashboard.views.customer import CustomerView
from dashboard.views.area import AreaView
from dashboard.views.sell import SellView, CreateSellView
from dashboard.views.deposite import DepositeView, TransactionView
from dashboard.views.purchase import PurchaseView, CreatePurchaseView

app_name= 'dashboard'

urlpatterns = [
    path('', DashboardView.as_view(), name="dashboard_url"),
    path('customer/', CustomerView.as_view(), name="customer_url"),
    path('area/', AreaView.as_view(), name="area_url"),
    path('deposite/', DepositeView.as_view(), name="deposite_url"),
    path('sell/', SellView.as_view(), name="sell_url"),
    path('create-sell/', CreateSellView.as_view(), name="create_sell_url"),
    path('transaction/', TransactionView.as_view(), name="transaction_url"),
    path('purchase/', PurchaseView.as_view(), name="purchase_url"),
    path('create-purchase/', CreatePurchaseView.as_view(), name="create_purchase_url"),




]


