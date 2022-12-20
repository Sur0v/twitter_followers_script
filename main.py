import requests
import json
import pandas as pd
import xlwt
import openpyxl
from datetime import datetime
import os
from openpyxl import load_workbook
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
from mplcursors import cursor
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import cufflinks as cf
import plotly.express as px

init_notebook_mode(connected=True)
cf.go_offline()

sns.set()
# %matplotlib inline

initiation = 0  #
xyz = []
date = []  # List of time variables
timing = str(datetime.now())
date.append(timing[5:19])  #List slicing on string element

username = "" #Twitter_username
url = 'https://api.twitter.com/2/users/by/username/' + username

#Request
r = requests.get(
  url,
  headers={
    'Authorization':
    '' #Bearer API
  })

#Response
response = json.loads(r.text)

url = 'https://api.twitter.com/2/users/' + response["data"][
  "id"] + '?user.fields=public_metrics,created_at,pinned_tweet_id&expansions=pinned_tweet_id&tweet.fields=created_at,public_metrics,source,context_annotations,entities'

r = requests.get(
  url,
  headers={
    'Authorization':
    '' #Bearer API
  })
response = json.loads(r.text)
totalFollower = int(response["data"]["public_metrics"]["followers_count"])

try:
  initiation = len(pd.read_excel('pandas_to_excel.xlsx'))

except:
  initiation = 0

print(initiation)

if initiation == 0:
  pd.ExcelWriter('pandas_to_excel.xlsx', datetime_format='dd/mm/yy')
  df = pd.DataFrame({'Follower': [totalFollower], 'Date': timing[5:19]})
  df.to_excel('pandas_to_excel.xlsx',
              sheet_name='new_sheet_name',
              columns={'Follower', 'Date'})

else:
  xyz = pd.read_excel("pandas_to_excel.xlsx")

  pd.ExcelWriter('pandas_to_excel.xlsx', datetime_format='dd/mm/yy')
  df = pd.DataFrame({'Follower': [totalFollower], 'Date': timing[5:19]})
  df2 = pd.concat([xyz,
                   df])  #adding two dataframes .apply function is depreceated.
  df2.to_excel('pandas_to_excel.xlsx',
               sheet_name='new_sheet_name',
               columns={'Follower', 'Date'})

twitter_df = pd.read_excel("pandas_to_excel.xlsx")

#Visualization with Seaborn

#figure=sns.lineplot(data=twitter_df , x="Date", y="Follower",marker=".")
#figure.set_ylim((twitter_df["Follower"].min())*0.98,(twitter_df["Follower"].max())*1.02)
#figure.set_title("Followers")
#plt.xticks(rotation=90)

#cursor(hover=True)
#plt.show()

#Basic Plotly Visualization
#twitter_df.iplot(kind='scatter',x='Date',y='Follower',mode='markers',size=10)

fig = px.line(twitter_df,
              x="Date",
              y="Follower",
              title='Number of Twitter Followers')
fig.show()
