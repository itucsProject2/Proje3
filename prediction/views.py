from django.shortcuts import render
from datetime import date, timedelta
import datetime
import csv
from django.http import HttpResponse
from prediction.models import Data, Date_Group
from pprint import pprint
import xlsxwriter

def readData(request):
    if Data.objects.all().count() > 20:
         arrange()
         return HttpResponse("Calisiyo hocam devam et")
    else:
         Data.objects.all().delete()
         #pprint('readDataya girdik')
         with open("example.csv", newline = '') as f:
             reader = csv.reader(f)
             next(reader)
             
             for row in reader:
                temptime = datetime.datetime.strptime(row[0],'%d-%m-%Y').strftime('%Y-%m-%d')
                #pprint(str(temptime))
                newrow = Data(tarih = temptime, magaza = row[1], lokasyon = row[2], kod = row[3], urunAdi = row[4], anaGrup = row[5], altGrup = row[6], urunCesidi = row[7], miktar = row[8])
                newrow.save()
                
         arrange()
         #excelwrite()
    
         return HttpResponse("Calisiyo hocam devam et")
 
 
def arrange():
    Date_Group.objects.all().delete()
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
    sheet1.write(0,1,'35000212',hformat)
    sheet1.write(0,2,'31001045',hformat)
    sheet1.write(0,3,'35000313',hformat)
    sheet1.write(0,4,'31000368',hformat)
     
    urun = [35000212, 31001045, 35000313, 31000368]
    
    for i in range(0, 4):
        date = datetime.date(2016,5,1)
        j = 1
        dcount = 0
        while date < datetime.date(2017, 4, 17):
            dcount = dcount + 1
            #pprint("TARIH = " + str(date) + "  i = " + str(i))
            data = Data.objects.filter(tarih = date, kod = urun[i])
            if data.count() > 0:
                sum = 0
                for foo in data:
                    sum += foo.miktar
                
                if i == 0:
                    sheet1.write(j,0,str(date),format)
                sheet1.write(j,i+1,sum,format)
                j = j + 1
                newval = Date_Group(tarih = date, kod = urun[i], miktar = sum)
                newval.save()
            else:
                if i == 0:
                    sheet1.write(j,0,str(date),format)
                sheet1.write(j,i+1,0,format)
                j += 1
            date = date + timedelta(days = 1)
            
    chart = book.add_chart({'type': 'line'})
    chart.add_series({
         'values': ['Sheet 1', 1, 1, dcount-1, 1],
         'categories' : ['Sheet 1', 1, 0, dcount-1, 0],
         'line' : {'color': 'blue'},
         'name' : '1',
            })
    chart.add_series({
         'values': ['Sheet 1', 1, 2, dcount-1, 2],
         'line' : {'color': 'red'},
         'name' : '2',
            })
    chart.add_series({
         'values': ['Sheet 1', 1, 3, dcount-1, 3],
         'line' : {'color': 'yellow'},
         'name' : '3',
            })
    chart.add_series({
         'values': ['Sheet 1', 1, 4, dcount-1, 4],
         'line' : {'color': 'green'},
         'name' : '4',
            })
    
    chart.set_size({'x_scale' : 4, 'y_scale' : 2})
    sheet1.set_column(0, 0, 15)
    sheet1.insert_chart('F1', chart)
    book.close()
    
    
def excelwrite():
     data = Date_Group.objects.all().values()   
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
     sheet1.write(0,1,'35000212',hformat)
     sheet1.write(0,2,'31001045',hformat)
     sheet1.write(0,3,'35000313',hformat)
     sheet1.write(0,4,'31000368',hformat)
     
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
 
             
