from django.shortcuts import render
from datetime import date
import csv
from django.http import HttpResponse
from prediction.models import Data
from pprint import pprint
import xlsxwriter

def readData(request):
     Data.objects.all().delete()
     with open("train.csv", newline = '') as f:
         reader = csv.reader(f)
         next(reader)
         for row in reader:
            if row[0] == "1":
                newrow = Data(date = row[2], location = row[0], amount = row[3])
                newrow.save()
     excelwrite()
     temp = "YALAK"
     return HttpResponse(temp)
 
def excelwrite():
     data = Data.objects.filter(location = "1")    
     book = xlsxwriter.Workbook('output.xlsx')

     hformat = book.add_format()
     hformat.set_align('center')
     hformat.set_align('vcenter')
     hformat.set_bold()

     format = book.add_format()
     format.set_align('center')
     format.set_align('vcenter')

     sheet1 = book.add_worksheet('Sheet 1')
     sheet1.write(0,0,'DATE',hformat)
     sheet1.write(0,1,'lOCATION',hformat)
     #sheet1.write(0,2,'PRODUCT',hformat)
     sheet1.write(0,2,'AMOUNT',hformat)
     
     i = 1
     for temp in data:
         sheet1.write(i,0,str(temp.date),format) 
         sheet1.write(i,1,str(temp.location),format)
         sheet1.write(i,2,temp.amount,format)
         sheet1.write(i,3,2000,format)
         i += 1
     chart = book.add_chart({'type': 'line'})
     chart.add_series({
         'values': ['Sheet 1', 1, 2, i-1, 2],
         'categories' : ['Sheet 1', 1, 0, i-1, 0],
         'line' : {'color': 'blue'},
         'name' : 'Real Amount',
            })
     chart.add_series({
         'values': ['Sheet 1', 1, 3, i-1, 3],
         'line' : {'color': 'red'},
         'name' : 'Predicted Amount',
            })
    
     chart.set_size({'x_scale' : 3, 'y_scale' : 1.5})
     sheet1.insert_chart('E1', chart)
     book.close()
 
             
