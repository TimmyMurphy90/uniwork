#!/usr/bin/env python
# coding: utf-8

# In[22]:


import os
import pandas as pd
import numpy as np
os.chdir("/Users/timothy/Downloads/AP Data set 21-22 2")


# In[28]:


df.head()


# In[29]:


df = df.set_index('id')


# In[26]:


df = pd.read_csv("airports.csv")


# In[27]:


df.head()


# In[20]:


df_newColumn = df


# In[14]:


to_drop = ['continent',
          'iso_region',
          'scheduled_service',
          'gps_code',
          'iata_code',
          'home_link',
          'wikipedia_link',
          'keywords',
          ]
df.drop(to_drop, inplace=True, axis=1)


# In[15]:


df


# In[17]:


closed_type = df['type']

closed = closed_type.str.contains('closed')
closed[:5]


# In[ ]:




