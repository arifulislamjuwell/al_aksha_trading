import datetime
from io import BytesIO
import openpyxl
from django.db import connection
from django.http import HttpResponse
from utils.transaction import my_transasction_dict_make
from dashboard.models import MyTransaction


def last_day_of_month(any_month):
    next_month = any_month.replace(
        day=28) + datetime.timedelta(days=4)  # this will never fail
    return next_month - datetime.timedelta(days=next_month.day)


def my_transaction_download(month):
    transactions= MyTransaction.objects.filter(created_at__year = month.split('-')[0], created_at__month = month.split('-')[1])
    final_data = my_transasction_dict_make(transactions, 0)
    print(final_data,'---------')
    sheet_name = 'My Transaction'
    starting_row = 2
    output = BytesIO()


[{'id': 4, 'date': datetime.date(2022, 6, 3), 'transaction_type': 'DEPOSIT', 'quantity': '', 'details': ' fghdf', 'total_bill': '', 'paid': 100, 'type_': 2, 'current_balance': 100}] 


    workbook = openpyxl.load_workbook(filename='sample/my_transaction_sample.xlsx')
    sheet = workbook.worksheets[0]

    for record in final_data:
        value_index = 0
        for column in range(1, 7):
            sheet.cell(row=starting_row,column=column).value = list(record.keys())[0]
            value_index += 1
        starting_row += 1

    workbook.save(output)
    output.seek(0)

    filename = str(sheet_name) + ".xlsx"
    content_disposition = "attachment; filename={}".format(filename)
    response = HttpResponse(output.read(
    ), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = content_disposition

    return response
