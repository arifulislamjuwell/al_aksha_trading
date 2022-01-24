from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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
def get_my_cur_balance():
    curr= MyTransaction.objects.all().order_by('-id')
    return curr[0].current_balance if curr.exists() else 0

class MyTransaction(models.Model):
    transaction_type= models.PositiveSmallIntegerField(choices= TRANSACTION_TYPE)
    amount= models.IntegerField()
    current_balance= models.IntegerField(default=0)
    created_at= models.DateField(auto_now_add=True)
    description= models.TextField(null=True)
    quantity= models.IntegerField(blank= True, null=True)


class MyDeposite(models.Model):
    amount= models.IntegerField()
    created_at= models.DateField( auto_now_add=True)
    note= models.TextField(null= True)

@receiver(post_save, sender=MyDeposite)
def update_my_deposite_transaction(sender, instance, created, **kwargs):
    if created:
        my_transaction= MyTransaction()
        my_transaction.transaction_type = DEPOSITE
        my_transaction.amount= instance.amount
        cur= get_my_cur_balance()
        my_transaction.current_balance= int(cur) + int(instance.amount)
        my_transaction.description= instance.note
        my_transaction.save()

class Purchase(models.Model):
    sub_total= models.IntegerField()
    paid= models.IntegerField()
    cement_type= models.PositiveSmallIntegerField(choices= CEMENT_TYPE)
    quantity= models.IntegerField()
    unit_price= models.FloatField()
    created_at= models.DateField( auto_now_add=True)

@receiver(post_save, sender=Purchase)
def update_my_transaction(sender, instance, created, **kwargs):
    if created:
        stock= Stock.objects.first()
        if instance.cement_type == OPC:
            stock.opc += instance.quantity
            description= 'OPC50KG(BAG)'
        else:
            stock.pcc += instance.quantity
            description= 'PCC50KG(BAG)'
        stock.save()
        total_amount= instance.sub_total
        paid_amount= 0
        try:
            my_transaction= MyTransaction.objects.all().order_by('-id')[0]
        except:
            my_transaction= None

        if my_transaction:
            if my_transaction.current_balance != 0:
                if paid_amount == 0:
                    if my_transaction.current_balance ==  total_amount:
                        my_transaction= MyTransaction()
                        my_transaction.transaction_type = BUY
                        my_transaction.amount= total_amount
                        cur= get_my_cur_balance()
                        my_transaction.save()
                        my_transaction.current_balance = int(cur) + (-total_amount)
                        my_transaction.description= description
                        my_transaction.quantity= instance.quantity
                        my_transaction.save()
                        
                    if my_transaction.current_balance > total_amount or (my_transaction.current_balance < total_amount):
                        my_transaction= MyTransaction()
                        my_transaction.transaction_type = BUY
                        my_transaction.amount= total_amount
                        cur= get_my_cur_balance()
                        my_transaction.save()
                        my_transaction.current_balance = int(cur) + (-total_amount)
                        my_transaction.description= description
                        my_transaction.quantity= instance.quantity
                        my_transaction.save()
                else:
                    deposite= MyDeposite()
                    deposite.amount = paid_amount
                    deposite.save()

                    my_transaction= MyTransaction()
                    my_transaction.transaction_type = BUY
                    my_transaction.amount= total_amount
                    cur= get_my_cur_balance()
                    my_transaction.save()
                    my_transaction.current_balance = int(cur) + (-total_amount)
                    my_transaction.description= description
                    my_transaction.quantity= instance.quantity

                    my_transaction.save()
                
        else:
            if total_amount == paid_amount:
                my_transaction= MyTransaction()
                my_transaction.transaction_type = BUY
                my_transaction.amount= total_amount
                my_transaction.current_balance = 0
                my_transaction.description= description
                my_transaction.quantity= instance.quantity
                my_transaction.save()

            if paid_amount != 0:
                if total_amount > paid_amount:
                    deposite= MyDeposite()
                    deposite.amount = paid_amount
                    deposite.save()

                    my_transaction= MyTransaction()
                    my_transaction.transaction_type = BUY
                    my_transaction.amount= total_amount
                    cur= get_my_cur_balance()
                    my_transaction.save()
                    my_transaction.current_balance = int(cur) + (-int(total_amount))
                    my_transaction.description= description
                    my_transaction.quantity= instance.quantity
                    my_transaction.save()
                else:
                    deposite= MyDeposite()
                    deposite.amount = paid_amount
                    deposite.save()

                    my_transaction= MyTransaction()
                    my_transaction.transaction_type = BUY
                    my_transaction.amount= total_amount
                    cur= get_my_cur_balance()
                    my_transaction.save()
                    my_transaction.current_balance = int(cur) + (-int(total_amount))
                    my_transaction.description= description
                    my_transaction.quantity= instance.quantity
                    my_transaction.save()  
            else:
                my_transaction= MyTransaction()
                my_transaction.transaction_type = BUY
                my_transaction.amount= total_amount
                cur= get_my_cur_balance()
                my_transaction.save()
                my_transaction.current_balance = int(cur) + (-int(total_amount))
                my_transaction.description= description
                my_transaction.quantity= instance.quantity
                my_transaction.save()


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
    quantity= models.IntegerField(blank= True, null=True)
    description= models.TextField(null=True)



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
            description= 'OPC50KG(BAG)'
        else:
            stock.pcc -= instance.quantity
            description= 'OPC50KG(BAG)'
        stock.save()
 
        total_amount= instance.total_bill
        paid_amount= instance.paid_amount
        try:
            customer_transaction= CustomerTransaction.objects.filter(customer= instance.customer).order_by('-created_at')[0]
        except:
            customer_transaction= None

        if customer_transaction:
            if customer_transaction.current_balance != 0:
                if paid_amount == 0:
                    if customer_transaction.current_balance == total_amount:
                        customer_t= CustomerTransaction()
                        customer_t.customer=  instance.customer
                        customer_t.transaction_type = BUY
                        customer_t.amount= total_amount
                        customer_t.quantity= instance.quantity
                        customer_t.description= description
                        cur= get_cur_balance(instance.customer)
                        customer_t.save()
                        customer_t.current_balance = int(cur) + (-total_amount)
                        customer_t.save()

                    if customer_transaction.current_balance > total_amount or (customer_transaction.current_balance < total_amount):
                        customer_t= CustomerTransaction()
                        customer_t.customer=  instance.customer
                        customer_t.transaction_type = BUY
                        customer_t.amount= total_amount
                        customer_t.quantity= instance.quantity
                        customer_t.description= description
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
                    customer_t.quantity= instance.quantity
                    customer_t.description= description

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
                customer_t.current_balance = 0
                customer_t.quantity= instance.quantity
                customer_t.description= description
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
                    customer_t.quantity= instance.quantity
                    customer_t.description= description
                    cur= get_cur_balance(instance.customer)
                    customer_t.save()
                    customer_t.current_balance = int(cur) + (-int(total_amount))
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
                    customer_t.quantity= instance.quantity
                    customer_t.description= description
                    cur= get_cur_balance(instance.customer)
                    customer_t.save()
                    customer_t.current_balance = int(cur) + (-int(total_amount))
                    customer_t.save()
            else:
                customer_t= CustomerTransaction()
                customer_t.customer=  instance.customer
                customer_t.transaction_type = BUY
                customer_t.amount= total_amount
                customer_t.quantity= instance.quantity
                customer_t.description= description
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


class MyRevenue(models.Model):
    date= models.DateField(auto_now=False, auto_now_add=False)
    total_sell= models.IntegerField(default= 0)
    total_purchase= models.IntegerField(default= 0)
    total_revenue= models.IntegerField(default= 0)


class Commission(models.Model):
    date= models.DateField(auto_now_add=True)
    amount= models.IntegerField()
    unit_amount= models.FloatField()
    note= models.CharField(max_length=250)

@receiver(post_save, sender=Commission)
def commission_transaction_update(sender, instance, created, **kwargs):
    if created:
        my_transaction= MyTransaction()
        my_transaction.transaction_type = COMMISSION
        my_transaction.amount= instance.amount
        cur= get_my_cur_balance()
        my_transaction.current_balance= int(cur) + int(instance.amount)
        my_transaction.description= instance.note
        my_transaction.save()

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
