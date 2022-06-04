#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pymysql

import pandas as pd
import numpy as np
import random
import base64
import calendar

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import dash
from jupyter_dash import JupyterDash
from dash.exceptions import PreventUpdate
from dash import Dash, dash_table
from dash import Input, Output, State, html
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

get_ipython().run_line_magic('load_ext', 'sql')


# In[2]:


get_ipython().run_line_magic('sql', 'mysql://dspuser:dsp@2021!@202.144.157.56/dsp_db')
data = get_ipython().run_line_magic('sql', 'SELECT * FROM student_dtls JOIN students_courses ON students_courses.student_id=student_dtls.student_id JOIN course_master ON course_master.id=students_courses.course_id JOIN dessung_profile ON dessung_profile.cid=student_dtls.cid JOIN dzongkhag_master ON dzongkhag_master.id = dessung_profile.dzongkhag_id JOIN qualifications_master ON qualifications_master.id=dessung_profile.qualification_id;')
t=pd.DataFrame(data)
t.rename(columns={8:'CID #',10:'DOB',11:'Email',14:'Name',27:'Programme',35:'DID',38:'Sex',47:'Dzongkhag',49:'Qualification'},inplace=True)
df=t[['CID #','Name','Programme','DID','Sex','Dzongkhag','Qualification']]


# In[3]:


app = dash.Dash(external_stylesheets=[dbc.themes.JOURNAL, dbc.icons.FONT_AWESOME])
app.title = "DSP Dashboard"  
server = app.server


# In[4]:


app.layout= dbc.Container([
    html.Div([
            html.H1(children='De-suung Skilling Programme Dashboard',
                    style = {'font-family': 'Comic Sans MS','textAlign':'center','color':'#fcba03','fontsize':60}
            )],
            className='col-8',
            style = {'padding-top' : '4%'}
        ),
    dbc.Button('Draw',id='start',color='info',size="lg", style={'width':'420px'}),
    dcc.Graph('graphex')
])


# In[5]:


@app.callback(
    Output('graphex','figure'),
    Input('start', 'n_clicks')
)

def on_button_click(n):
    if n is None:
        fig = go.Figure()
    else:
        g = df[['Sex']].value_counts().to_frame(name = 'number')
        g.reset_index(inplace = True)
        fig = px.bar(g, x= 'Sex', y = 'number', color = 'Sex')
    return fig


# In[ ]:


if __name__ == '__main__':
    port = 5000 + random.randint(0, 999)    
    url = "http://127.0.0.1:{0}".format(port)    
    app.run_server(use_reloader=False, debug=True, port=port)


# In[ ]:



