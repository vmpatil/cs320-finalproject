#!/usr/bin/env python
# coding: utf-8

# In[33]:


import pandas as pd
import geopandas as gpd
from matplotlib import pyplot as plt
import math


# In[ ]:


# Referenced from https://datascience.quantecon.org/applications/maps.html


# In[7]:


state_df = gpd.read_file("http://www2.census.gov/geo/tiger/GENZ2016/shp/cb_2016_us_state_5m.zip")
state_df.head()


# In[8]:


county_df = gpd.read_file("http://www2.census.gov/geo/tiger/GENZ2016/shp/cb_2016_us_county_5m.zip")
county_df.head()


# In[9]:


county_df = county_df.query("STATEFP == '55'")
fig, gax = plt.subplots(figsize=(10, 10))

state_df.query("NAME == 'Wisconsin'").plot(ax=gax, edgecolor="black", color="white")
county_df.plot(ax=gax, edgecolor="black", color="white")

plt.show()


# In[35]:


temp=pd.read_csv('Area_avg_5year.csv')
temp = temp.drop(["Unnamed: 0"], axis = 1)
temp.index = ["2014", "2015", "2016", "2017", "2018"]


# In[36]:


import statistics 
Co_re = {"County" : [], "avg" : []}
for c in temp.columns:
    Co_re["County"].append(c)
    Co_re["avg"].append(statistics.mean(list(temp[c])))


# In[37]:


results = pd.DataFrame(Co_re)
results


# In[41]:


results["avg"] = results["avg"].map(lambda x: math.log(x + 20))
results


# In[42]:


results["County"] = results["County"].str.title()
results["County"] = results["County"].str.strip()
county_df["NAME"] = county_df["NAME"].str.title()
county_df["NAME"] = county_df["NAME"].str.strip()


# In[43]:


res_w_states = county_df.merge(results, left_on="NAME", right_on="County", how="inner")


# In[44]:


res_w_states


# In[60]:


import matplotlib.colors as mcolors

cdict = {'red':   ((0.0, 0.0, 0.0),
                   (0.5, 0.0, 0.0),
                   (1.0, 1.0, 1.0)),
         'blue':  ((0.0, 0.0, 0.0),
                   (1.0, 0.0, 0.0)),
         'green': ((0.0, 0.0, 1.0),
                   (0.5, 0.0, 0.0),
                   (1.0, 0.0, 0.0))}

cmap = mcolors.LinearSegmentedColormap(
'my_colormap', cdict, 100)


# In[66]:


fig, gax = plt.subplots(figsize = (10,8))

# Plot the state
state_df[state_df['NAME'] == 'Wisconsin'].plot(ax = gax, edgecolor='black',color='white')

# Plot the counties and pass 'rel_trump_share' as the data to color
res_w_states.plot(
    ax=gax, edgecolor='black', column='avg', legend=True, cmap="RdYlGn_r",
)

# I don't want the axis with long and lat
plt.axis('off')

plt.show()
gax.get_figure().savefig("fig1.svg", bbox_inches="tight")


# In[ ]:




