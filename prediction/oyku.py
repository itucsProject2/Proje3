from pandas import Series
from matplotlib import python 
from django.http import HttpResponse



def oyku(request):
    series = Series.from_csv("example.csv", header = 0)
    series.plot()
    return HttpResponse(str(series))