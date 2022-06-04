from dashboard.models import BUY,DEPOSITE

def my_transasction_dict_make(transactions, current_balance):

    row_list = []
    for transaction in transactions:
        dic= {}
        content_object = transaction.content_object
        dic ={'id': content_object.id }
        if transaction.transaction_type == BUY:
            sub_total = content_object.sub_total
            quantity = content_object.quantity
            dic['date'] = content_object.created_at
            dic['transaction_type'] = 'Purchase'
            dic['quantity'] = quantity
            dic['details'] = '{} BAGS-50KG({})'.format(quantity,content_object.get_cement_type_display())
            dic['total_bill'] = sub_total
            dic['paid'] = 0
            dic['type_'] = 1
            current_balance = current_balance - sub_total
            dic['current_balance'] = current_balance

        elif transaction.transaction_type == DEPOSITE:
            amount = content_object.amount
            dic['date'] = content_object.created_at
            dic['transaction_type'] = 'DEPOSIT'
            dic['quantity'] = ''
            dic['details'] = content_object.note
            dic['total_bill'] = ''
            dic['paid'] = amount
            dic['type_'] = 2
            current_balance = current_balance  + amount
            dic['current_balance'] = current_balance
        
        else:
            amount = content_object.amount
            dic['date'] = content_object.date
            dic['transaction_type'] = 'COMMISSION'
            dic['quantity'] = ''
            dic['details'] = content_object.note
            dic['total_bill'] = ''
            dic['paid'] = amount
            dic['type_'] = 3
            current_balance = current_balance  + amount
            dic['current_balance'] = current_balance 

        row_list.append(dic)
    return row_list

def customer_transasction_dict_make(transactions, current_balance):
    row_list = []
    for transaction in transactions:
        content_object = transaction.content_object
        dic= {}
        dic ={'id': content_object.id }
        if transaction.transaction_type == BUY:
            total_bill = content_object.total_bill
            paid_amount =  content_object.paid_amount
            quantity = content_object.quantity
            dic['date'] = content_object.created_at
            dic['transaction_type'] = 'BUY'
            dic['quantity'] = quantity
            dic['details'] = '{} BAGS-50KG({})'.format(quantity,content_object.get_cement_type_display())
            dic['date'] = content_object.created_at
            dic['total_bill'] = total_bill
            dic['type_'] = 1
            dic['paid'] = content_object.paid_amount
            current_balance = (current_balance - total_bill) + paid_amount
            dic['current_balance'] = current_balance

        else:
            amount = content_object.amount
            dic['date'] = content_object.created_at
            dic['transaction_type'] = 'DEPOSITE'
            dic['quantity'] = ''
            dic['details'] = content_object.note
            dic['date'] = content_object.created_at
            dic['total_bill'] = ''
            dic['paid'] = amount
            dic['type_'] = 2
            current_balance = current_balance  + amount
            dic['current_balance'] = current_balance

        row_list.append(dic)
    return row_list
