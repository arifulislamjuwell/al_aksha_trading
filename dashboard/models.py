from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.db.models import F
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Sum

OPC= 1
PCC= 2
CEMENT_TYPE= (
    (OPC, 'OPC'),
    (PCC, 'PCC')
)
DEPOSITE=1
BUY=2
COMMISSION= 3

PURCHASE = ((1, 'OPC'),
               (2, 'PCC'))


TRANSACTION_TYPE= (
    (DEPOSITE, 'Deposite'),
    (BUY, 'Buy'),
    (COMMISSION, 'Commission'),

)
PLUS =1
MINUS = 2


class OpeningInformation(models.Model):
    pcc= models.IntegerField(default = 0)
    opc= models.IntegerField(default = 0)
    my_balance_type = models.IntegerField(default = MINUS)
    my_balance = models.IntegerField(default = 0)


class MyRevenue(models.Model):
    date= models.DateField(auto_now=False, auto_now_add=False)
    total_sell= models.IntegerField(default= 0)
    total_purchase= models.IntegerField(default= 0)
    total_revenue= models.IntegerField(default= 0)

class MyTransaction(models.Model):
    transaction_type= models.PositiveSmallIntegerField(choices= TRANSACTION_TYPE)
    created_at= models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


class Commission(models.Model):
    date= models.DateField(auto_now_add=True)
    amount= models.IntegerField()
    unit_amount= models.FloatField()
    note= models.CharField(max_length=250)
    my_transactions = GenericRelation(MyTransaction)


class MyDeposite(models.Model):
    amount= models.IntegerField()
    created_at= models.DateField( auto_now_add=False)
    note= models.TextField(null= True)
    my_transactions = GenericRelation(MyTransaction)


class Purchase(models.Model):
    sub_total= models.IntegerField()
    cement_type= models.PositiveSmallIntegerField(choices= CEMENT_TYPE)
    quantity= models.IntegerField()
    unit_price= models.FloatField()
    created_at= models.DateField( auto_now_add=False)
    my_transactions = GenericRelation(MyTransaction)


@receiver(post_save, sender=Purchase)
@receiver(post_save, sender=MyDeposite)
@receiver(post_save, sender=Commission)
def my_transaction(sender, instance, created, **kwargs):
    if created:
        transaction = MyTransaction()
        transaction_type= BUY if sender == Purchase else DEPOSITE
        if sender == Commission:
            transaction_type = COMMISSION
        transaction.transaction_type = transaction_type
        transaction.content_object = instance
        transaction.save()


class Area(models.Model):
    name= models.CharField(max_length=50)

# Create your models here.
class Customer(models.Model):
    name= models.CharField( max_length=50)
    phone_number= models.CharField(max_length=50)
    address= models.TextField()
    email= models.CharField(max_length=50)
    opening_balance= models.IntegerField(default = 0)
    opening_balance_type= models.PositiveSmallIntegerField(default = MINUS)
    area= models.ForeignKey(Area, related_name="customers", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def current_balance(self):
        opening_balance = -self.opening_balance if self.opening_balance_type == MINUS else self.opening_balance
        total_buy_and_paid = self.sells.all().aggregate(Sum('total_bill'), Sum('paid_amount'))
        total_bill =  total_buy_and_paid.get('total_bill__sum') if  total_buy_and_paid.get('total_bill__sum') else 0
        total_paid = total_buy_and_paid.get('paid_amount__sum') if total_buy_and_paid.get('paid_amount__sum') else 0
        total_deposit = self.customer_deposites.all().aggregate(Sum('amount'))
        total_deposit =  total_deposit.get('amount__sum') if total_deposit.get('amount__sum') else 0
        return (opening_balance - total_bill) + total_paid + total_deposit

class CustomerTransaction(models.Model):
    customer= models.ForeignKey(Customer,related_name='transaction', on_delete=models.CASCADE)
    transaction_type= models.PositiveSmallIntegerField(choices= TRANSACTION_TYPE)
    created_at= models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self):
        return self.customer.name + 'id:-'+ str(self.id)


class Sell(models.Model):
    customer= models.ForeignKey(Customer,related_name="sells", on_delete=models.CASCADE)
    cement_type= models.PositiveSmallIntegerField(choices= CEMENT_TYPE)
    quantity= models.IntegerField()
    unit_price = models.FloatField()
    total_bill= models.IntegerField(default= 0)
    paid_amount= models.IntegerField(default= 0)
    created_at= models.DateField(auto_now_add=False)
    customer_transactions = GenericRelation(CustomerTransaction)


class CustomerDeposit(models.Model):
    customer= models.ForeignKey(Customer,related_name='customer_deposites', on_delete=models.CASCADE, null=True)
    amount= models.IntegerField()
    created_at= models.DateField( auto_now_add=False)
    note = models.TextField()
    customer_transactions = GenericRelation(CustomerTransaction)

@receiver(post_save, sender=CustomerDeposit)
@receiver(post_save, sender=Sell)
def customer_transaction(sender, instance, created, **kwargs):
    if created:
        transaction = CustomerTransaction()
        transaction.customer = instance.customer
        transaction.transaction_type = BUY if sender == Sell else DEPOSITE
        transaction.content_object = instance
        transaction.save()



class Revenue(models.Model):
    customer= models.ForeignKey(Customer, related_name="revenues", on_delete=models.CASCADE)
    date= models.DateField(auto_now=False, auto_now_add=False)
    pcc_sell= models.IntegerField(default= 0)
    opc_sell= models.IntegerField(default= 0)
    pcc_purchase= models.IntegerField(default= 0)
    opc_purchase= models.IntegerField(default= 0)
    revenue= models.IntegerField(default= 0)

    @property
    def total_sell(self):
        return self.opc_sell + self.pcc_sell
    
    @property
    def total_purchase(self):
        return self.pcc_purchase + self.opc_purchase

@receiver(post_save, sender=Revenue)
def upddate_my_revenue(sender, instance, created, **kwargs):
    exists= MyRevenue.objects.filter(date__month= instance.date.month, date__year= instance.date.year)
    if exists:
        rev_obj= exists.first()
    else:
        rev_obj= MyRevenue()
        rev_obj.date= instance.date

    revenue= 0
    for rev in Revenue.objects.filter(date__month= instance.date.month, date__year= instance.date.year):
        revenue+= rev.revenue

    rev_obj.total_sell= instance.total_sell
    rev_obj.total_purchase= instance.total_purchase
    rev_obj.total_revenue= revenue
    rev_obj.save()
