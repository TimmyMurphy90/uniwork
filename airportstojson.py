#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[10]:


csv_file = r'/Users/timothy/Downloads/AP Data set 21-22 2/airports.csv'
runways_df = pd.read_csv(csv_file)


# In[11]:


json_output = r'/Users/timothy/Downloads/AP Data set 21-22 2/airports.json'
output = runways_df.to_json(json_output, indent = 1, orient= 'records')


# In[ ]:




