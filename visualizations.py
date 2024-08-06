#!/usr/bin/env python
# coding: utf-8

# In[5]:


from plotnine import *


# In[8]:


import polars as pl

# Importing Boto3 library to access AWS resources
import boto3
from io import BytesIO

# Specify the S3 URI
s3_uri = 's3://rplace-data-naj/Diff_in_variance/bots_active.parquet'

# Split the S3 URI into bucket and key
bucket, key = s3_uri.replace('s3://', '').split('/', 1)

# Accessing the S3 bucket
s3 = boto3.client('s3')

# Read the Parquet file from S3 into a DataFrame
with BytesIO() as f:
    s3.download_fileobj(bucket, key, f)
    f.seek(0)
    df = pl.read_parquet(f)

# Display the first few rows of the DataFrame
df.head()


# In[18]:


df_counts = df.groupby('user').count().sort(by='count', descending = False).to_pandas()


# In[ ]:





# In[2]:


import numpy as np
import pandas as pd

bins = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, np.inf]
names = ['1', '2', '3', '4', '5', '6','7','8','9','10+']

df_counts['bins'] = pd.cut(df_counts['count'], bins, labels=names)
df_counts.head()


# In[83]:


df_counts.groupby('bins').value_counts().reset_index(drop=True, inplace=True)


# In[84]:


df_counts_2


# In[85]:


(ggplot(df_counts,
aes(
  x = "bins"
))
+ geom_bar()

 + geom_bar(fill='#FF5700')
 + labs(title='Bot Activity Distribution based on Pixels Changed', x='Number of Pixels Changed') 
 + theme(panel_background=element_rect(fill='white'))
)


# In[31]:


# Visual 2
df


# In[47]:


df_color = df.groupby('pixel_color').count().to_pandas()
df_color.head()


# In[43]:


top_pixels = df_color.sort_values(by = "count", ascending = False).head()
pixels_list = top_pixels['count'].value_counts().index.tolist()

(ggplot(top_pixels,
aes(
  x = "pixel_color"
))
+ geom_bar()
 + theme_bw()
 + geom_bar(fill='#FF5700')
 + labs(title='Bot Activity Distribution based on Pixels Changed', x='Number of Pixels Changed') 
)


# In[44]:


pixels_list


# In[45]:


top_pixels


# In[67]:


top_pixels = df_color.sort_values(by = "count", ascending = False).head()

pixels_list = top_pixels['pixel_color'].value_counts().index.tolist() # orders from greatest to least

(ggplot(top_pixels, mapping = aes(
  x = "pixel_color",
    y = 'count',
    fill = 'pixel_color'
))
+ geom_bar(stat = 'identity',colour = 'black')
 + geom_text(aes(label = 'count'), nudge_y=0.05*max(top_pixels['count']), color='black') 
  + labs(x = "Pixel Color", y = "Number of Uses", title = "Top Five Pixel Colors Used by Bots")
  + scale_x_discrete(limits=pixels_list)
  + scale_fill_manual(values=['#000000', '#00A368', '#FF4500', '#FFD635', '#FFFFFF'])
  + theme(panel_background=element_rect(fill='white'))
  + guides(fill = False)
)


# In[10]:


data = {
    'Day': ['Day1 (20th)', 'Day2 (21st)', 'Day3 (22nd)', 'Day4 (23rd)', 'Day5 (24th)', 'Day6 (25th)'],
    'Count': [17997, 16977, 17092, 18867, 58806, 30684]
}

df_corrected = pd.DataFrame(data)
df_corrected


# In[13]:


from plotnine import *
import pandas as pd
import numpy as np


# In[18]:


plot2 = (ggplot(df_corrected, aes(x = 'Day', y = 'Count')) +
        geom_bar(stat = 'identity', fill = '#FF5700') +
        geom_text(aes(label = 'Count'), nudge_y=0.05*max(df_corrected['Count']), color='black') +
        theme(axis_text_x = element_text(rotation=45, hjust = 1), panel_background = element_rect(fill='white')) + 
        labs(title='Bot Activity through Pixel Placement Per Day', x='Day', y='Count'))


print(plot2)

