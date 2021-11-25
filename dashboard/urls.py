
from django.contrib import admin
from django.urls import path, include

from dashboard.views.dashboard import DashboardView
from dashboard.views.customer import CustomerView
from dashboard.views.area import AreaView

app_name= 'dashboard'

urlpatterns = [
    path('', DashboardView.as_view(), name="dashboard_url"),
    path('customer/', CustomerView.as_view(), name="customer_url"),
    path('area/', AreaView.as_view(), name="area_url")
]


