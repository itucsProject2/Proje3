import pandas as pd
import numpy as np
from django.http import HttpResponse
from matplotlib import pyplot
from statsmodels.tsa.ar_model import AR
from statsmodels.tsa.arima_model import ARIMA
from pprint import pprint
import xlrd
from sklearn.metrics import mean_squared_error
from numpy.linalg import  LinAlgError

def koray(request):
    #fields = ['Gun', 'SatisMiktari']
    #df = pd.read_csv("example.csv", usecols = fields)

    xl = pd.ExcelFile("aylik.xlsx")
    #xl.sheet_names = [u'Alinan Veriler', u'Haftelik', u'Aylik']
    df = xl.parse("Sayfa1", header=0, index_col= 0, parse_cols=[0, 1], converters={'a':float}, squeeze=True)
    pprint(df.head(25))
    #df.plot()
    #pyplot.show()
    data = df
    pprint("DATA")
    pprint(data)
    pprint("SONUC")
    X = data.values
    #size = int(len(X) * 0.66)
    #train, test = X[0:size], X[size:len(X)]
    #history = [X for x in train]
    #predictions = list()
    train, test = X[1:len(X)-2], X[len(X)-2:]
    model = AR(train)
    model_fit = model.fit()
    predictions = model_fit.predict(start = len(train), end = len(train)+len(test)-1, dynamic = False)
    
    for i in range(len(predictions)):
    #for i in range(len(test)):
        #fitting
        #model  = ARIMA(data, order = (15, 2, 0))
        #model_fit = model.fit(disp = 0) # disp = 0, debug info gostermiyor
        #pprint(model_fit.summary())
        #plot
        #outcome = model_fit.forecast()
        pprint("SONUC")
        #pprint(outcome[0])
        pprint(predictions[i])
    #model = AR(df)
    #model_fit = model.fit()
    #prediction = model_fit.predict(start = len(dataset, end = len(dataset)))
    #pprint(str(prediction))
    return HttpResponse("OPTUM CANIM")