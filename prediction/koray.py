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

#def koray(request):
def prediction():
    xl = pd.ExcelFile("temp.xlsx")
    adata = xl.parse("Sayfa1", header=0, parse_cols=[0, 1], index_col= 0, converters={'a':float}, squeeze=True)
    bdata = xl.parse("Sayfa1", header=0, parse_cols=[0, 2], index_col= 0, converters={'b':float}, squeeze=True)
    
    pprint('adata')
    pprint(adata)
    pprint("bdata")
    pprint(bdata)

    predictions = list()
    predictionsb = list()
    for i in range(0, 2):
        if i == 0:
            data = adata
        elif i == 1:
            data = bdata
            
        pprint("DATA")
        pprint(data)
        X = data.values
        size = int(len(X) * 0.66)
        train, test = X[0:size], X[size:len(X)]

        #train, test = X[1:len(X)-5], X[len(X)-5:]
        #model = AR(train)
        #model_fit = model.fit()
        #predictions = model_fit.predict(start = len(train), end = len(train)+len(test)-1, dynamic = False)
        
        #for i in range(len(predictions)):
        for j in range(0, 12):
        #for i in range(len(test)):
            #data.drop(data.count)
            #count = data.count()
            #data = data.drop(data.index[count-1])
            #fitting
            model  = ARIMA(data, order = (5, 1, 0))
            model_fit = model.fit(disp = 0) # disp = 0, debug info gostermiyor
            #pprint(model_fit.summary())
            #plot
            outcome = model_fit.forecast()
            if i == 0:
                predictions = [outcome[0]] + predictions
            elif i == 1:
                predictionsb = [outcome[0]] + predictionsb
            count = data.count()
            data = data.drop(data.index[count-1])
            
        predictions = predictions + predictionsb
        pprint("Sonuc")
        for j in range(0, len(predictions)):
            pprint(predictions[j])
        #pprint(predictions[i] * predictions[i])
    #model = AR(df)
    #model_fit = model.fit()
    #prediction = model_fit.predict(start = len(dataset, end = len(dataset)))
    #pprint(str(prediction))
    return predictions
    #return HttpResponse("OPTUM CANIM")