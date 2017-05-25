import pandas as pd
from django.http import HttpResponse
from matplotlib import pyplot
from statsmodels.tsa.ar_model import AR
from statsmodels.tsa.arima_model import ARIMA
from pprint import pprint
import xlrd

def koray(request):
    #fields = ['Gun', 'SatisMiktari']
    #df = pd.read_csv("example.csv", usecols = fields)

    xl = pd.ExcelFile("koray.xlsx")
    #xl.sheet_names = [u'Alinan Veriler', u'Haftelik', u'Aylik']
    df = xl.parse("Sayfa1", header=0, index_col= 0, parse_cols=[0, 1], converters={'a':float}, squeeze=True)
    pprint(df.head(25))
    #df.plot()
    #pyplot.show()
    pprint("SONUC")
    for i in range(len(df)):
        #fitting
        model  = ARIMA(df, order = (30, 2, 0))
        model_fit = model.fit(disp = 0) # disp = 0, debug info gostermiyor
        #pprint(model_fit.summary())
        #plot
        outcome = model_fit.forecast()
        #pprint("SONUC")
        pprint(outcome[0])
    
    #model = AR(df)
    #model_fit = model.fit()
    #prediction = model_fit.predict(start = len(dataset, end = len(dataset)))
    #pprint(str(prediction))
    return HttpResponse("OPTUM CANIM")