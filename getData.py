import requests
from pprint import pprint
import pandas as pd
import json
from pandas.io.json import json_normalize
from bokeh.embed import components
from bokeh.plotting import figure, output_file, show


r = requests.get('https://www.quandl.com/api/v3/datasets/WIKI/GOOG.json?start_date=2016-11-01&end_date=2016-11-30&api_key=mD1dWJVXSgcJy_2xkdEp',auth=('user','pass')) 
status = r.status_code
#print status
stocks_json = r.json()

stocks_json = stocks_json['dataset']

columns = stocks_json['column_names']
data = stocks_json['data']
stocks_df = pd.DataFrame(data,columns=columns)
stocks_df['Date'] = pd.to_datetime(stocks_df['Date'])

color_list = ['blue','red','green','purple']
name_list = ['High','Low','Open','Close']

output_file('plot.html')
p = figure(width=800, height=500, x_axis_type='datetime')
for i in xrange(len(name_list)):
    p.line(stocks_df['Date'],stocks_df[name_list[i]],legend=name_list[i],line_color=color_list[i])
show(p)