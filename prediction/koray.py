from pandas import Series
from django.http import HttpResponse
from matplotlib import python

def koray(request):
    series = Series.from_csv("example.csv", header = 0)
    series.plot()
    
    return HttpResponse(str(series))