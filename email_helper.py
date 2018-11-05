#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 09:58:08 2018

@author: dallums
"""



import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

        
        
def constructFormattedEmail(_user, 
                   _pwd, 
                   _from, 
                   _to, 
                   _subject, 
                   _data_dict):
    
    MESSAGE = MIMEMultipart('alternative')
    MESSAGE['subject'] = _subject
    MESSAGE['To'] = _to
    MESSAGE['From'] = _from
     
    html = """
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
      <title>html title</title>
      <style type="text/css" media="screen">
        table, th, td {
           table-layout: fixed;
           width: 200px;
           text-align: left;
           border: 1px solid black;
        }
        th {          
            background-color: #6699ff;
            color: white;
        }
        tr:nth-child(even) {background-color: #f2f2f2;}
        tr:hover {background-color: #8c8c8c;}
      </style>
    </head>
    <body>
     <p>Hello,</p>
     <p>Here is your data:</p>
    """

    table = pd.DataFrame.from_dict(data=_data_dict, 
                                   orient='index').T.to_html(index=False)
      
    html = html + table + """</body>"""

    HTML_BODY = MIMEText(html, 
                         'html')
    MESSAGE.attach(HTML_BODY)
    
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(_user, 
                     _pwd)
        server.sendmail(_from, 
                        _to, 
                        str(MESSAGE))
        server.close()
    
        print('Email sent!')
        
    except Exception as exception:
        print("Error: %s!\n\n" % exception)
    


if __name__ == '__main__':
    user = '' # email address here
    user_pwd = '' # password here
    to = user # can change to separate address
    subject = "Model Tuning Results"
    d = {'Nodes': [5, 3, 6, 7], 
         'Epochs': [50, 75, 85, 100],
         'Learning Rate': [.05, .05, .05, .005],
         'Optimizer': ['Adam', 'Adam', 'Adam', 'Mae'],
         'RMSE': [45, 46, 47, 43]}
    
    constructFormattedEmail(_user=user, 
                   _pwd=user_pwd, 
                   _from=user, 
                   _to=to, 
                   _subject=subject, 
                   _data_dict=d)

