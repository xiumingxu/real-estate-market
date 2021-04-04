#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import pandas_profiling as pp
import fbprophet
from fbprophet.plot import plot_plotly, plot_components_plotly


# In[2]:


# load the zipcodes we are focusing on. It is formatted with column names as [zipcode, city, rank]
zipcodes = pd.read_csv('zipcodes.csv')
# My dataset strips the leading 0 from zipcodes, which happens to be what the other dataset came as too. Since they both do this, the sets can still be compared without additional work (unlike R)
zipcodes['zipcode'] = zipcodes['zipcode'].astype(str)

#load the listing data
data = pd.read_csv('downloads/RDC_Inventory_Core_Metrics_Zip_History.csv', header=0, parse_dates=True, low_memory=False)[:-2] # remove last two rows, which have shown themselvse as weird
data['year-month'] = pd.to_datetime(data['month_date_yyyymm'], format='%Y%m')


# In[3]:


local_data = data[data['postal_code'].isin(zipcodes['zipcode'])]
local_listing_sum = local_data[['year-month', 'active_listing_count']].groupby(['year-month']).sum().reset_index().rename(columns = {'year-month': 'ds', 'active_listing_count': 'y'})


# In[4]:


profile = pp.ProfileReport(local_data, 'mls profile report')


# In[5]:


local_listing_sum.tail() # looks good


# In[6]:


m = fbprophet.Prophet()
# we have an inventory floor of 0, so let's establish that
local_listing_sum['floor'] = 0
m.fit(local_listing_sum)
# future does NOT predict, it simply makes timestamps into the future on a monthly frequency
future = m.make_future_dataframe(periods=12, freq = 'MS')


# In[7]:


forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(15)


# In[8]:


fig1 = m.plot(forecast)
decomp_plot = m.plot_components(forecast)

