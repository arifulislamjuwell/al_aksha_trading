from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from multiselectfield import MultiSelectField

OPC= 1
PCC= 2
CEMENT_TYPE= (
    (OPC, 'OPC'),
    (PCC, 'PCC')
)
DEPOSITE=1
BUY=2
PURCHASE = ((1, 'OPC'),
               (2, 'PCC'))


TRANSACTION_TYPE= (
    (DEPOSITE, 'Deposite'),
    (BUY, 'Buy')
)


class Purchase(models.Model):
    sub_total= models.IntegerField()
    paid= models.IntegerField()
    cement_type= MultiSelectField(choices= PURCHASE)
    created_at= models.DateField( auto_now_add=True)


class OpcPurchase(models.Model):
    purchase= models.OneToOneField(Purchase , related_name= "opc_purchase",on_delete=models.CASCADE)
    quantity= models.IntegerField()
    unit_price= models.FloatField()
    total= models.IntegerField()


class PccPurchase(models.Model):
    purchase= models.OneToOneField(Purchase ,related_name= "pcc_purchase",on_delete=models.CASCADE)
    quantity= models.IntegerField()
    unit_price= models.FloatField()
    total= models.IntegerField()


def get_cur_balance(customer):
    curr= CustomerTransaction.objects.filter(customer= customer).order_by('-created_at')
    return curr[0].current_balance if curr.exists() else 0


class Area(models.Model):
    name= models.CharField(max_length=50)

# Create your models here.
class Customer(models.Model):
    name= models.CharField( max_length=50)
    phone_number= models.CharField(max_length=50)
    address= models.TextField()
    email= models.CharField(max_length=50)
    area= models.ForeignKey(Area, related_name="customers", on_delete=models.CASCADE)


class CustomerTransaction(models.Model):
    customer= models.ForeignKey(Customer,related_name='transaction', on_delete=models.CASCADE)
    transaction_type= models.PositiveSmallIntegerField(choices= TRANSACTION_TYPE)
    amount= models.IntegerField()
    current_balance= models.IntegerField(default=0)
    created_at= models.DateTimeField(auto_now_add=True)


class Sell(models.Model):
    customer= models.ForeignKey(Customer,related_name="sells", on_delete=models.CASCADE)
    cement_type= models.PositiveSmallIntegerField(choices= CEMENT_TYPE)
    quantity= models.IntegerField()
    unit_price = models.FloatField()
    delivery_address= models.TextField(null=True)
    total_bill= models.IntegerField(default= 0)
    paid_amount= models.IntegerField(default= 0)
    created_at= models.DateField( auto_now_add=True)

@receiver(post_save, sender=Sell)
def update_transaction(sender, instance, created, **kwargs):
    if created:
        stock= Stock.objects.first()

        if instance.cement_type == OPC:
            stock.opc -= instance.quantity

        else:
            stock.pcc -= instance.quantity
            stock.save()
 
        transaction_type= None
        total_amount= instance.total_bill
        paid_amount= instance.paid_amount
        try:
            customer_transaction= CustomerTransaction.objects.filter(customer= instance.customer).order_by('-created_at')[0]
        except:
            customer_transaction= None

        if customer_transaction:
            if customer_transaction.current_balance != 0:
                if paid_amount == 0:
                    if customer_transaction.current_balance > total_amount or (customer_transaction.current_balance < total_amount):
                        customer_t= CustomerTransaction()
                        customer_t.customer=  instance.customer
                        customer_t.transaction_type = BUY
                        customer_t.amount= total_amount
                        cur= get_cur_balance(instance.customer)
                        customer_t.save()
                        customer_t.current_balance = int(cur) + (-total_amount)
                        customer_t.save()
                else:
                    deposite= Deposite()
                    deposite.amount = paid_amount
                    deposite.customer= instance.customer
                    deposite.save()

                    customer_t= CustomerTransaction()
                    customer_t.customer=  instance.customer
                    customer_t.transaction_type = BUY
                    customer_t.amount= total_amount
                    cur= get_cur_balance(instance.customer)
                    customer_t.save()
                    customer_t.current_balance = int(cur) + (-total_amount)
                    customer_t.save()
                
        else:
            if total_amount == paid_amount:
                customer_t= CustomerTransaction()
                customer_t.customer=  instance.customer
                customer_t.transaction_type = BUY
                customer_t.amount= total_amount
                cur= get_cur_balance(instance.customer)
                customer_t.save()
                customer_t.current_balance = int(cur) + (-total_amount)
                customer_t.save()

            if paid_amount != 0:
                if total_amount > paid_amount:
                    deposite= Deposite()
                    deposite.amount = paid_amount
                    deposite.customer= instance.customer
                    deposite.save()

                    customer_t= CustomerTransaction()
                    customer_t.customer=  instance.customer
                    customer_t.transaction_type = BUY
                    customer_t.amount= total_amount

                    cur= get_cur_balance(instance.customer)

                    customer_t.save()
                    customer_t.current_balance = int(cur) + (-int(total_amount))
                    customer_t.save()
            else:
                customer_t= CustomerTransaction()
                customer_t.customer=  instance.customer
                customer_t.transaction_type = BUY
                customer_t.amount= total_amount

                cur= get_cur_balance(instance.customer)

                customer_t.save()
                customer_t.current_balance = int(cur) + (-int(total_amount))
                customer_t.save()


class Deposite(models.Model):
    customer= models.ForeignKey(Customer,related_name='deposites', on_delete=models.CASCADE, null=True)
    amount= models.IntegerField()
    created_at= models.DateField( auto_now_add=True)


@receiver(post_save, sender=Deposite)
def update_transaction(sender, instance, created, **kwargs):
    if created:
        customer_t= CustomerTransaction()
        customer_t.customer=  instance.customer
        customer_t.transaction_type = DEPOSITE
        customer_t.amount= instance.amount
        cur= get_cur_balance(instance.customer)
        customer_t.current_balance= int(cur) + int(instance.amount)
        customer_t.save()

class Stock(models.Model):
    pcc= models.IntegerField(default= 0)
    opc= models.IntegerField(default= 0)



@receiver(post_save, sender=OpcPurchase)
def opc_stock_update(sender, instance, created, **kwargs):
    if created:
        stock= Stock.objects.first()
        stock.opc += int(instance.quantity)
        stock.save()

@receiver(post_save, sender=PccPurchase)
def pcc_stock_update(sender, instance, created, **kwargs):
    if created:
        stock= Stock.objects.first()
        stock.pcc += int(instance.quantity)
        stock.save()
 

class Commission(models.Model):
    date= models.DateField(auto_now_add=True)
    amount= models.IntegerField()
    unit_amount= models.IntegerField()


class MyyTransaction(models.Model):
    transaction_type= models.PositiveSmallIntegerField(choices= TRANSACTION_TYPE)
    amount= models.IntegerField()
    current_balance= models.IntegerField(default=0)
    created_at= models.DateTimeField(auto_now_add=True)