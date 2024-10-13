#!/usr/bin/env python
# coding: utf-8

# In[47]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_webpage(url: str): 
    try:
        res = requests.get(url)
        return res.content
    except Exception as e:
        print(f"Error while fetching: {e}")


def parse_html(html: str):
    soup = BeautifulSoup(html,"html.parser")
    df = pd.read_html(str(soup.table))[0]
    df.rename(columns={"DATES" : "dates", "Unnamed: 2": "text", "DAYS": "dow"}, inplace=True)
    return df


html = fetch_webpage('https://www.ccny.cuny.edu/registrar/fall')
parse_html(html)


# In[ ]:




