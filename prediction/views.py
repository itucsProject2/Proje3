from django.shortcuts import render
from datetime import date, timedelta
import datetime
import csv
from django.http import HttpResponse
from prediction.models import Data, Date_Group
from pprint import pprint
import xlsxwriter


def showGraph(request):
    return render(request, 'index.html')

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

    sheet1 = book.add_worksheet('Alinan Veriler')
    sheet2 = book.add_worksheet('Haftalik')
    sheet3 = book.add_worksheet('Aylik')
    
    sheet1.write(0,0,'Tarih',hformat)
    sheet1.write(0,1,'Urun 1',hformat)
    sheet1.write(0,2,'Urun 2',hformat)
     
    urun = [35000212, 31001045]
    counter = 0
    haftac = 0;
    haftaici = [0] * 200
    haftasonu = [0] * 200
    hafta = [0] * 200
    for i in range(0, 2):
        if i==1:
            haftac = counter
            sheet2.write(counter,0,counter,format)
            sheet2.write(counter,1,0,format)
            sheet2.write(counter,2,0,format)
            sheet2.write(counter,3,0,format)
            counter+=1
        date = datetime.date(2016,5,2)
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
            
            if i==0 or i==1:
                if (dcount % 7) == 0:
                    haftasonu[counter] = haftasonu[counter] + sum
                    hafta[counter] = haftasonu[counter] + haftaici[counter]
                    haftasonu[counter] = haftasonu[counter] / 2
                    haftaici[counter] = haftaici[counter] / 5
                    if i==1:
                        sheet2.write(counter,0,counter-haftac,format)
                    else:
                        sheet2.write(counter,0,counter,format)
                        
                    sheet2.write(counter,1,haftaici[counter],format)
                    sheet2.write(counter,2,haftasonu[counter],format)
                    sheet2.write(counter,3,hafta[counter],format)
                    counter+=1
                elif dcount % 7 < 6:
                    haftaici[counter] = haftaici[counter] + sum
                else:
                    haftasonu[counter] = haftasonu[counter] + sum 
                
            date = date + timedelta(days = 1)   
    
# haftalik
    # urun 1
    charthafta1 = book.add_chart({'type' : 'column'})
    
    sheet2.write(0,0,'Hafta',hformat)
    sheet2.write(0,1,'H. Ici Ort',hformat)
    sheet2.write(0,2,'H. Sonu Ort',hformat)
    sheet2.write(0,3,'Toplam',hformat)
    
    charthafta1.add_series({
         'values': ['Haftalik', 1, 1, haftac, 1],
         'categories' : ['Haftalik', 1, 0, haftac, 0],
         'column' : {'color': 'blue'},
         'name' : 'Hafta Ici',
            })
    charthafta1.add_series({
         'values': ['Haftalik', 1, 2, haftac, 2],
         'column' : {'color': 'red'},
         'name' : 'Hafta Sonu',
            })
    charthafta1.set_x_axis({
    'name': 'Hafta',
    'num_font':  {'italic': True },
})
    charthafta1.set_title({
    'name': '1. Urun',
})
    charthafta1.set_size({'x_scale' : 3})
    sheet2.insert_chart('E1', charthafta1)
    
    # urun 2
    charthafta2 = book.add_chart({'type' : 'column'})
    charthafta2.add_series({
         'values': ['Haftalik', haftac+1, 1, counter, 1],
         'categories' : ['Haftalik', 1, 0, haftac, 0],
         'column' : {'color': 'blue'},
         'name' : 'Hafta Ici',
            })
    charthafta2.add_series({
         'values': ['Haftalik', haftac+1, 2, counter, 2],
         'column' : {'color': 'red'},
         'name' : 'Hafta Sonu',
            })
    charthafta2.set_title({
    'name': '2. Urun',
})
    charthafta2.set_x_axis({
    'name': 'Hafta',
    'num_font':  {'italic': True },
})
    charthafta2.set_size({'x_scale' : 3})
    sheet2.insert_chart('E19', charthafta2)
    
    charthafta = book.add_chart({'type' : 'line'})
    
    charthafta.add_series({
         'values': ['Haftalik', 1, 3, haftac, 3],
         'categories' : ['Haftalik', 1, 0, haftac, 0],
         'line' : {'color': 'blue'},
         'name' : '1. Urun',
            })
    charthafta.add_series({
         'values': ['Haftalik', haftac+1, 3, counter, 3],
         'linr' : {'color': 'red'},
         'name' : '2. Urun',
            })
    charthafta.set_title({
    'name': 'Haftalik Toplam',
})
    charthafta.set_size({'x_scale' : 3})
    charthafta.set_x_axis({
    'name': 'Hafta',
    'num_font':  {'italic': True },
})

    sheet2.insert_chart('E34', charthafta)
    
# haftalik

# aylik
    sheet3.write(0,0,'Ay',hformat)
    sheet3.write(0,1,'Urun 1 - G',hformat)
    sheet3.write(0,2,'Urun 2 - G',hformat)
    sheet3.write(0,3,'Urun 1 - A',hformat)
    sheet3.write(0,4,'Urun 2 - A',hformat)
    aygunsayar = [30,30,31,31,30,31,30,31,31,28,31,16]
    a1 = 12 *[0]
    a2 = 12 *[0]
    aylar = ["May", "Haz", "Tem", "Agu", "Eyl", "Eki" , "Kas", "Ara", "Oca", "Sub", "Mar", "Nis"]
    aycounter = 0
    tempcount = 0
    data = Date_Group.objects.values()
    for d in data:
        ay = d['tarih'].month
        if ay < 5:
            ay = ay + 7
        else:
            ay = ay - 5
            
        if d['kod'] == 35000212:
            a1[ay] += d['miktar']
        elif d['kod'] == 31001045:
            a2[ay] += d['miktar']
            
            
    sheet3.write_column('D2', a1,format)
    sheet3.write_column('E2', a2,format)
    
    
    for i in range(0,12):
        a1[i] = a1[i] / aygunsayar[i]
        a2[i] = a2[i] / aygunsayar[i]
        
    sheet3.write_column('A2', aylar,format)
    sheet3.write_column('B2', a1,format)
    sheet3.write_column('C2', a2,format)
    
    chartay = book.add_chart({'type': 'line'})

    
    chartay.add_series({
        'values': ['Aylik', 1, 1, 12, 1],
         'categories' : ['Aylik', 1, 0, 12, 0],
         'line' : {'color': 'blue'},
         'name' : 'Urun 1',
        })
    
    chartay.add_series({
        'values': ['Aylik', 1, 2, 12, 2],
         'line' : {'color': 'red'},
         'name' : 'Urun 2',
        })
    chartay.set_size({'x_scale' : 2, 'y_scale' : 1.5})
    chartay.set_title({
    'name': 'Ortalama Satis Miktari (Gunluk Ortalama)',
})
    sheet3.insert_chart('F1', chartay)
    
    chartay2 = book.add_chart({'type': 'line'})
    chartay2.add_series({
        'values': ['Aylik', 1, 3, 12, 3],
        'categories' : ['Aylik', 1, 0, 12, 0],
         'line' : {'color': 'blue'},
         'name' : 'Urun 1',
        })
    
    chartay2.add_series({
        'values': ['Aylik', 1, 4, 12, 4],
         'line' : {'color': 'red'},
         'name' : 'Urun 2',
        })
    chartay2.set_size({'x_scale' : 2, 'y_scale' : 1.5})
    chartay2.set_title({
    'name': 'Ortalama Satis Miktari (Aylik Net)',
})
    sheet3.insert_chart('F23', chartay2)
# aylik



         
    chart = book.add_chart({'type': 'line'})
    chart.add_series({
         'values': ['Alinan Veriler', 1, 1, dcount-1, 1],
         'categories' : ['Alinan Veriler', 1, 0, dcount-1, 0],
         'line' : {'color': 'blue'},
         'name' : 'Urun 1',
            })
    chart.add_series({
         'values': ['Alinan Veriler', 1, 2, dcount-1, 2],
         'line' : {'color': 'red'},
         'name' : 'Urun 2',
            })
    chart.set_title({
    'name': 'Tum Veriler',
})
    chart.set_size({'x_scale' : 3, 'y_scale' : 1.5})
    sheet1.set_column(0, 0, 15)
    sheet1.insert_chart('D1', chart)
    
    book.close()

             
