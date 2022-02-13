from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.db.models import F


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
class MyBalance(models.Model):
    purchase_amount = models.IntegerField(default=0)
    paid_amount = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'Purchase: {self.purchase_amount}, Paid: {self.paid_amount}'

    @property
    def due_amount(self):
        return self.paid_amount - self.purchase_amount if  self.purchase_amount  > self.paid_amount else 0
    
    @property
    def current_balance(self):
        # return self.total_purchase_amount - self.total_paid_amount
        return self.paid_amount - self.purchase_amount


class MyTransaction(models.Model):
    transaction_type= models.PositiveSmallIntegerField(choices= TRANSACTION_TYPE)
    bill= models.IntegerField(default=0)
    paid= models.IntegerField(default=0)
    created_at= models.DateField(auto_now_add=True)
    description= models.TextField(null=True)
    quantity= models.IntegerField(blank= True, null=True)
    purchase_dependency_id= models.CharField(max_length=10, null= True)
    deposit_dependency_id= models.CharField(max_length=10, null= True)
    commission_dependency_id= models.CharField(max_length=10, null= True)

@receiver(post_save, sender=MyTransaction)
def update_my_balance(sender, instance, created, **kwargs):
    if created:
        balance= MyBalance.objects.first()
        if balance is None:
            balance = MyBalance()
            balance.save()
        balance.purchase_amount = F('purchase_amount') + instance.bill
        balance.paid_amount= F('paid_amount') + instance.paid
        balance.save()

@receiver(pre_delete, sender=MyTransaction)
def back_previous_my_transaction_remove(sender, instance, using, **kwargs):
    balance = MyBalance.objects.first()
    balance.purchase_amount = F('purchase_amount') - instance.bill
    balance.paid_amount= F('paid_amount') - instance.paid
    balance.save()

class MyDeposite(models.Model):
    amount= models.IntegerField()
    created_at= models.DateField( auto_now_add=False)
    purchase_dependency_id =  models.CharField(max_length=10, null= True)
    note= models.TextField(null= True)

@receiver(post_save, sender=MyDeposite)
def update_my_deposite_transaction(sender, instance, created, **kwargs):
    if created:
        my_transaction= MyTransaction()
        my_transaction.transaction_type = DEPOSITE
        my_transaction.paid= instance.amount
        my_transaction.description= instance.note
        my_transaction.deposit_dependency_id = str(instance.id)
        my_transaction.save()

@receiver(pre_delete, sender=MyDeposite)
def back_previous_my_deposit_remove(sender, instance, using, **kwargs):
    MyTransaction.objects.filter(deposit_dependency_id = str(instance.id)).delete()


class Purchase(models.Model):
    sub_total= models.IntegerField()
    paid= models.IntegerField()
    cement_type= models.PositiveSmallIntegerField(choices= CEMENT_TYPE)
    quantity= models.IntegerField()
    unit_price= models.FloatField()
    created_at= models.DateField( auto_now_add=False)

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

        purchase_id= instance.id
        final_bill = instance.sub_total
        paid_amount = instance.paid

        if paid_amount > final_bill:
            deposit_amount= paid_amount - final_bill
            create_my_transaction(paid=final_bill, bill=final_bill, quantity= instance.quantity, description= description, purchase_dependency_id=purchase_id)
            create_my_deposit_record(deposit_amount, instance.created_at, purchase_id)
        else:
            create_my_transaction( paid=paid_amount, bill=final_bill, quantity= instance.quantity, description= description, purchase_dependency_id=purchase_id)

@receiver(pre_delete, sender=Purchase)
def back_previous_purchase_remove(sender, instance, using, **kwargs):
    stock= Stock.objects.first()
    if instance.cement_type == OPC:
        stock.opc-= instance.quantity
    else:
        stock.pcc -= instance.quantity
    stock.save()
    purchase_id= str(instance.id)
    MyTransaction.objects.filter(purchase_dependency_id = purchase_id).delete()
    MyDeposite.objects.filter(purchase_dependency_id = purchase_id).delete()

class Area(models.Model):
    name= models.CharField(max_length=50)

# Create your models here.
class Customer(models.Model):
    name= models.CharField( max_length=50)
    phone_number= models.CharField(max_length=50)
    address= models.TextField()
    email= models.CharField(max_length=50)
    area= models.ForeignKey(Area, related_name="customers", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class CustomerTransaction(models.Model):
    customer= models.ForeignKey(Customer,related_name='transaction', on_delete=models.CASCADE)
    transaction_type= models.PositiveSmallIntegerField(choices= TRANSACTION_TYPE)
    bill= models.IntegerField(default=0)
    paid= models.IntegerField(default=0)
    created_at= models.DateTimeField(auto_now_add=True)
    quantity= models.IntegerField(blank= True, null=True)
    description= models.TextField(null=True)
    sell_dependency_id= models.CharField(max_length=10, null= True)
    deposit_dependency_id= models.CharField(max_length=10, null= True)

    def __str__(self):
        return self.customer.name + 'id:-'+ str(self.id)

def create_transaction(customer, paid, bill, quantity, description, sell_dependency_id= None):
    customer_t = CustomerTransaction()
    customer_t.customer = customer
    customer_t.bill= bill
    customer_t.transaction_type = BUY
    customer_t.quantity = quantity
    customer_t.paid = paid
    customer_t.description= description
    customer_t.sell_dependency_id= sell_dependency_id
    customer_t.save()

def create_my_transaction( paid, bill, quantity, description, purchase_dependency_id= None):
    customer_t = MyTransaction()
    customer_t.bill= bill
    customer_t.transaction_type = BUY
    customer_t.quantity = quantity
    customer_t.paid = paid
    customer_t.description= description
    customer_t.purchase_dependency_id= purchase_dependency_id
    customer_t.save()

def create_deposit_record(customer, amount, created_at, sell_dependency_id= None):
    Deposite.objects.create(
        customer=customer,
        amount=amount,
        sell_dependency_id= sell_dependency_id,
        created_at= created_at
    )

def create_my_deposit_record(amount, created_at, purchase_dependency_id= None):
    MyDeposite.objects.create(
        amount=amount,
        purchase_dependency_id= purchase_dependency_id,
        created_at= created_at
    )

class CustomerBalance(models.Model):
    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE, related_name='balance')
    total_purchase_amount = models.IntegerField(default=0)
    total_paid_amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.customer} | Purchase: {self.total_purchase_amount}, Paid: {self.total_paid_amount}'

    @property
    def due_amount(self):
        return self.total_paid_amount - self.total_purchase_amount
    
    @property
    def current_balance(self):
        # return self.total_purchase_amount - self.total_paid_amount
        return self.total_paid_amount - self.total_purchase_amount

@receiver(post_save, sender=CustomerTransaction)
def update_customer_balance(sender, instance, created, **kwargs):
    if created:
        balance, created= CustomerBalance.objects.get_or_create(customer= instance.customer)
        balance.total_purchase_amount = F('total_purchase_amount') + instance.bill
        balance.total_paid_amount= F('total_paid_amount') + instance.paid
        balance.save()

@receiver(pre_delete, sender=CustomerTransaction)
def back_previous_transaction_remove(sender, instance, using, **kwargs):
    balance, created= CustomerBalance.objects.get_or_create(customer= instance.customer)
    balance.total_purchase_amount = F('total_purchase_amount') - instance.bill
    balance.total_paid_amount= F('total_paid_amount') - instance.paid
    balance.save()

class Sell(models.Model):
    customer= models.ForeignKey(Customer,related_name="sells", on_delete=models.CASCADE)
    cement_type= models.PositiveSmallIntegerField(choices= CEMENT_TYPE)
    quantity= models.IntegerField()
    unit_price = models.FloatField()
    total_bill= models.IntegerField(default= 0)
    paid_amount= models.IntegerField(default= 0)
    created_at= models.DateField( auto_now_add=False)

@receiver(pre_delete, sender=Sell)
def back_previous_sell_remove(sender, instance, using, **kwargs):
    stock= Stock.objects.first()
    if instance.cement_type == OPC:
        stock.opc += instance.quantity
    else:
        stock.pcc += instance.quantity
    stock.save()
    sell_id= str(instance.id)
    CustomerTransaction.objects.filter(sell_dependency_id = sell_id).delete()
    Deposite.objects.filter(sell_dependency_id = sell_id).delete()


@receiver(post_save, sender=Sell)
def update_customer_transaction(sender, instance, created, **kwargs):
    if created:
        stock= Stock.objects.first()
        if instance.cement_type == OPC:
            stock.opc -= instance.quantity
            description= 'OPC50KG(BAG)'
        else:
            stock.pcc -= instance.quantity
            description= 'PCC50KG(BAG)'
        stock.save()

        sell_id= instance.id
        customer = instance.customer
        final_bill = instance.total_bill
        paid_amount = instance.paid_amount

        if paid_amount > final_bill:
            deposit_amount= paid_amount - final_bill
            create_transaction(customer=customer, paid=final_bill, bill=final_bill, quantity= instance.quantity, description= description, sell_dependency_id=sell_id)
            create_deposit_record(customer, deposit_amount, instance.created_at, sell_id)
        else:
            create_transaction(customer=customer, paid=paid_amount, bill=final_bill, quantity= instance.quantity, description= description, sell_dependency_id=sell_id)


class Deposite(models.Model):
    customer= models.ForeignKey(Customer,related_name='deposites', on_delete=models.CASCADE, null=True)
    amount= models.IntegerField()
    created_at= models.DateField( auto_now_add=False)
    sell_dependency_id= models.CharField(max_length=10, null= True)


@receiver(pre_delete, sender=Deposite)
def back_previous_deposit_remove(sender, instance, using, **kwargs):
    CustomerTransaction.objects.filter(deposit_dependency_id = str(instance.id)).delete()

@receiver(post_save, sender=Deposite)
def update_transaction(sender, instance, created, **kwargs):
    if created:
        customer_t= CustomerTransaction()
        customer_t.customer=  instance.customer
        customer_t.transaction_type = DEPOSITE
        customer_t.paid= instance.amount
        customer_t.deposit_dependency_id = instance.id
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
def update_my_commission_transaction(sender, instance, created, **kwargs):
    if created:
        my_transaction= MyTransaction()
        my_transaction.transaction_type = COMMISSION
        my_transaction.paid= instance.amount
        my_transaction.description= instance.note
        my_transaction.commission_dependency_id = str(instance.id)
        my_transaction.save()

@receiver(pre_delete, sender=Commission)
def back_previous_my_commission_remove(sender, instance, using, **kwargs):
    MyTransaction.objects.filter(commission_dependency_id = str(instance.id)).delete()


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
