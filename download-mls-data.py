c#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
from rea.utils import DBUpdater
import os, glob
import pandas as pd


# In[2]:


def download_csv(url, storage_path = ''):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """

    ua = UserAgent()
    header = {'User-Agent':str(ua.chrome)}
    prefix = 'https://www.realtor.'
    # storage_path = '/some/directory/' #you only need this in for G Cloud Storage
    files = []
    with requests.Session() as req:
        r = req.get(url, headers=header) # get download data source
        soup = BeautifulSoup(r.content, 'html.parser') #"""Beautiful Soup Elixir and Tonic - "The Screen-Scraper's Friend". http://www.crummy.com/software/BeautifulSoup/ Beautiful Soup uses a pluggable XML or HTML parser to parse a(possibly invalid) document into a tree representation. Beautiful Soupprovides methods and Pythonic idioms that make it easy to navigate,search, and modify the parse tree.
        target = [f"{url[:20]}{item['href']}" for item in soup.select(
            "a[href$='.csv']")] # target is the links on the websites
        for t in target:
            if t.startswith(prefix):
                t = t[len(prefix):]
            print(f"Downloading {t}")
            r = req.get(t)
            name = t.rsplit("/", 1)[-1]
            files.append(r.content)
            with open(name, 'wb') as f:
                f.write(r.content)

    return files


            # in a cloud function, prepend this with the directory of your cloud storage bucket


def properSep(data):
    return data.str.split('[,](?:\d)').apply(pd.Series)



def main():
    url = "https://www.realtor.com/research/data/"
    storage_path = '/downloads/'
    data = download_csv(url, storage_path)
    #
    # path = os.path.dirname(__file__)
    # extension = 'csv'
    # os.chdir(path)
    # result = glob.glob('*.{}'.format(extension))
    # # print(result)
    # db = DBUpdater(database="HOUSING")
    # specials=  ['RDC_Inventory_Core_Metrics_Zip_History.csv',
    #  'RDC_Inventory_Core_Metrics_County_History.csv',
    # 'RDC_Inventory_Hotness_Metrics_County_History.csv',
    # 'RDC_Inventory_Core_Metrics_Zip_History.csv',
    # 'RDC_Inventory_Core_Metrics_County.csv']
    #
    # files = ['listing_weekly_core_aggregate_by_country.csv',
    #          'RDC_Inventory_Core_Metrics_County_History.csv',
    #          'RDC_Inventory_Core_Metrics_County.csv'
    #          ]
    #
    # for file in result:
    #     db.save_csv(file)



# In[ ]:

main()

# add sql