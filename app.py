from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
import json
from bokeh.embed import components
from bokeh.plotting import figure, output_file, show

app = Flask(__name__)

app.vars = {}

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
    if request.method=='GET':
        return render_template('index.html')
    else:
        app.vars['ticker'] = request.form['ticker']
        try:
            app.vars['Open'] = request.form['open']
        except:
            app.vars['Open'] = 'off'
        try:
            app.vars['High'] = request.form['high']
        except:
            app.vars['High'] = 'off'
        try:
            app.vars['Low'] = request.form['low']
        except:
            app.vars['Low'] = 'off'
        try:
            app.vars['Close'] = request.form['close']
        except:
            app.vars['Close'] = 'off'
        app.vars['on'] = [key for key,value in app.vars.items() if value=='on']
        return redirect('/plot')

@app.route('/plot')
def plot():
    r = requests.get('https://www.quandl.com/api/v3/datasets/WIKI/%s.json?start_date=2016-11-01&end_date=2016-11-30&api_key=mD1dWJVXSgcJy_2xkdEp'%app.vars['ticker'],auth=('user','pass')) 
    stocks_json = r.json()
    columns = stocks_json['dataset']['column_names']
    data = stocks_json['dataset']['data']
    stocks_df = pd.DataFrame(data,columns=columns)
    stocks_df['Date'] = pd.to_datetime(stocks_df['Date'])
    
    color_list = ['blue','red','green','purple']
    name_list = app.vars['on']
    
    p = figure(width=800, height=500, x_axis_type='datetime',title='%s Stock Prices for November 2016'%app.vars['ticker'])
    p.title.align = 'center'
    p.title_text_font_size = '20pt'
    p.xaxis.major_label_text_font_size = '16pt'
    p.yaxis.major_label_text_font_size = '16pt'
    p.legend
    for i in xrange(len(name_list)):
        p.line(stocks_df['Date'],stocks_df[name_list[i]],legend=name_list[i],line_color=color_list[i])
    script,div = components(p)
    
    return render_template('plot.html',div=div,script=script)

if __name__ == '__main__':
  app.run(port=33507)
