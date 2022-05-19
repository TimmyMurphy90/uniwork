#!/usr/bin/env python
# coding: utf-8

# In[14]:


from pymongo import MongoClient
import json


# In[15]:


credentials = None
with open('/Users/timothy/Downloads/AP Data set 21-22 2/runways242.json') as f:
    credentials = json.load(f)


# In[16]:


myclient = MongoClient("mongodb://localhost:27017/")


# In[17]:


db = myclient["GFG"]


# In[18]:


Collection = db["data"]


# In[24]:


with open('/Users/timothy/Downloads/AP Data set 21-22 2/runways242.json') as file:
    file_data = json.load(file)


# In[25]:


if isinstance(file_data, list):
    Collection.insert_many(file_data)
else:
    Collection.insert_one(file_data)


# In[26]:


file_data


# In[ ]:




