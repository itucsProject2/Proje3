"""
    -> Time series data loaded "columns = Date, urun adi, satis miktari"
    -> 804 row for K
    -> 1078 row for L
    -> 1131 row for M
    -> 202 row for E
    
"""

import pandas as pd
import matplotlib as plt
from django.http import HttpResponse
from pprint import pprint

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
from statsmodels.tsa.arima_model import ARIMA




def oyku(request):
    
    fig = Figure()
    ax = fig.add_subplot(111)
    x=[]
    y=[]
    
    
    fields = ['Gun' ,'SaticiUrunAdi', 'SatisMiktari']
    df = pd.read_csv('example.csv', header = 0, parse_dates = [0], usecols=fields)
    k_df = df[(df.SaticiUrunAdi == 'K')][['Gun', 'SatisMiktari']]
    l_df = df[(df.SaticiUrunAdi == 'L')][['Gun', 'SatisMiktari']]
    m_df = df[(df.SaticiUrunAdi == 'M')][['Gun', 'SatisMiktari']]
    e_df = df[(df.SaticiUrunAdi == 'E')][['Gun', 'SatisMiktari']]
    pprint(k_df)
    x = k_df['Gun']
    y = k_df['SatisMiktari']
    
    ax.plot_date(x,y,'-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    ax.set_title("K graph")
    ax.set_xlabel("dates")
    ax.set_ylabel("satis miktari")
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type ='image/png')
    canvas.print_png(response)
    plt.pyplot.close(fig)
    
    model = ARIMA(k_df, order=(5,1,0))
    model_fit = model.fit(disp=0)
    
    
    
    
    
    
    
    
    return HttpResponse(response)








"""
(r'^(?P<poll_id>\d+)/results/result.png$', 'mysite.polls.views.plotResults')

my_plot = sales_totals.sort(columns='ext price',ascending=False).plot(kind='bar',legend=None,title="Total Sales by Customer")
my_plot.set_xlabel("Customers")
my_plot.set_ylabel("Sales ($)")

"""
