#!/usr/bin/env python
# coding: utf-8

# In[5]:


# import pandas as pd
# !pip install polars


# In[6]:


import polars as pl
import boto3
from io import BytesIO

# Specify the S3 URI
s3_uri = 's3://rplace-data-naj/Diff_in_variance/day1var.parquet'

# Split the S3 URI into bucket and key
bucket, key = s3_uri.replace('s3://', '').split('/', 1)

# Accessing the S3 bucket
s3 = boto3.client('s3')

# Read the Parquet file from S3 into a DataFrame
with BytesIO() as f:
    s3.download_fileobj(bucket, key, f)
    f.seek(0)
    df = pd.read_parquet(f)

# Display the first few rows of the DataFrame
df.head()


# In[3]:


# Specify the S3 URI
s3_uri = 's3://rplace-data-naj/Diff_in_variance/day2var.parquet'

# Split the S3 URI into bucket and key
bucket, key = s3_uri.replace('s3://', '').split('/', 1)

# Accessing the S3 bucket
s3 = boto3.client('s3')

# Read the Parquet file from S3 into a DataFrame
with BytesIO() as f:
    s3.download_fileobj(bucket, key, f)
    f.seek(0)
    df2 = pd.read_parquet(f)

# Display the first few rows of the DataFrame
df2.head()


# In[4]:


# Specify the S3 URI
s3_uri = 's3://rplace-data-naj/Diff_in_variance/day3var.parquet'

# Split the S3 URI into bucket and key
bucket, key = s3_uri.replace('s3://', '').split('/', 1)

# Accessing the S3 bucket
s3 = boto3.client('s3')

# Read the Parquet file from S3 into a DataFrame
with BytesIO() as f:
    s3.download_fileobj(bucket, key, f)
    f.seek(0)
    df3 = pd.read_parquet(f)

# Display the first few rows of the DataFrame
df3.head()


# In[5]:


# Specify the S3 URI
s3_uri = 's3://rplace-data-naj/Diff_in_variance/day4var.parquet'

# Split the S3 URI into bucket and key
bucket, key = s3_uri.replace('s3://', '').split('/', 1)

# Accessing the S3 bucket
s3 = boto3.client('s3')

# Read the Parquet file from S3 into a DataFrame
with BytesIO() as f:
    s3.download_fileobj(bucket, key, f)
    f.seek(0)
    df4 = pd.read_parquet(f)

# Display the first few rows of the DataFrame
df4.head()


# In[6]:


# Specify the S3 URI
s3_uri = 's3://rplace-data-naj/Diff_in_variance/day5var.parquet'

# Split the S3 URI into bucket and key
bucket, key = s3_uri.replace('s3://', '').split('/', 1)

# Accessing the S3 bucket
s3 = boto3.client('s3')

# Read the Parquet file from S3 into a DataFrame
with BytesIO() as f:
    s3.download_fileobj(bucket, key, f)
    f.seek(0)
    df5 = pd.read_parquet(f)

# Display the first few rows of the DataFrame
df5.head()


# In[ ]:





# In[7]:


# Specify the S3 URI
s3_uri = 's3://rplace-data-naj/Diff_in_variance/day6var.parquet'

# Split the S3 URI into bucket and key
bucket, key = s3_uri.replace('s3://', '').split('/', 1)

# Accessing the S3 bucket
s3 = boto3.client('s3')

# Read the Parquet file from S3 into a DataFrame
with BytesIO() as f:
    s3.download_fileobj(bucket, key, f)
    f.seek(0)
    df6 = pd.read_parquet(f)

# Display the first few rows of the DataFrame
df6.head()


# # Merge on User

# In[8]:


# df.merge(df2, on = "user", lsuffix = '_df1', rsuffix = '_df2', how = 'outer')
df.merge(df2, on = "user", how = 'outer')


# In[9]:


import pandas as pd

# Assuming 'df' and 'df2' are already loaded as shown in your snippet

# Merge df and df2 on the 'user' column
joined_df = pd.merge(df, df2, on='user', suffixes=('_day1', '_day2'), how = 'outer')
joined_df.fillna(0, inplace=True)

# If you need to sum counts from both days for each user, ensure your DataFrames have 'count' columns or similar
# Here's an example assuming you have 'count_day1' and 'count_day2' as resulting columns from the merge
joined_df['count'] = joined_df['count_day1'] + joined_df['count_day2']
#joined_df['variance_of_timestamp_diff'] = joined_df['variance_of_timestamp_diff_day1'] + joined_df['variance_of_timestamp_diff_day2']

# Display the result
joined_df = joined_df[['user', 'count', 'variance_of_timestamp_diff_day1', 'variance_of_timestamp_diff_day2']]
joined_df.head()


# In[11]:


joined_df2 = pd.merge(df3, df4, on='user', suffixes=('_day3', '_day4'), how = 'outer')
joined_df2.fillna(0, inplace=True)
joined_df2['count'] = joined_df2['count_day3'] + joined_df2['count_day4']

# Display the result
joined_df2 = joined_df2[['user', 'count', 'variance_of_timestamp_diff_day3', 'variance_of_timestamp_diff_day4']]
joined_df2.head()


# In[12]:


joined_df3 = pd.merge(df5, df6, on='user', suffixes=('_day5', '_day6'), how = 'outer')
joined_df3.fillna(0, inplace=True)
joined_df3['count'] = joined_df3['count_day5'] + joined_df3['count_day6']

# Display the result
joined_df3 = joined_df3[['user', 'count', 'variance_of_timestamp_diff_day5', 'variance_of_timestamp_diff_day6']]
joined_df3.head()


# In[14]:


test = pd.merge(joined_df, joined_df2, on='user', suffixes=('_a', '_b'), how = 'outer')
test.fillna(0, inplace=True)
test['count'] = test['count_a'] + test['count_b']
test = test[['user','count', 'variance_of_timestamp_diff_day1', 'variance_of_timestamp_diff_day2', 'variance_of_timestamp_diff_day3', 'variance_of_timestamp_diff_day4']]
test.head()


# In[15]:


finalmerge = pd.merge(test, joined_df3, on='user', suffixes=('_a', '_b'), how = 'outer')
finalmerge.fillna(0, inplace=True)
finalmerge['count'] = finalmerge['count_a'] + finalmerge['count_b']

finalmerge = finalmerge[['user','count', 'variance_of_timestamp_diff_day1', 'variance_of_timestamp_diff_day2', 'variance_of_timestamp_diff_day3', 'variance_of_timestamp_diff_day4', 'variance_of_timestamp_diff_day5', 'variance_of_timestamp_diff_day6']]
finalmerge.head()


# In[16]:


finalmerge # removed users that only clicked once and never came back


# In[17]:


finalmerge['variance_of_timestamp_diff_avg'] = (finalmerge['variance_of_timestamp_diff_day1'] + finalmerge['variance_of_timestamp_diff_day2'] + finalmerge['variance_of_timestamp_diff_day3'] + finalmerge['variance_of_timestamp_diff_day4'] + finalmerge['variance_of_timestamp_diff_day5'] + finalmerge['variance_of_timestamp_diff_day6'])/6
finalmerge = finalmerge[['user', 'count', 'variance_of_timestamp_diff_avg']]


# In[18]:


finalmerge.sort_values(by='variance_of_timestamp_diff_avg', ascending = True)


# In[19]:


finalmerge.sort_values(by='variance_of_timestamp_diff_avg', ascending = True).iloc[0:3322]


# In[20]:


finalmerge[finalmerge['variance_of_timestamp_diff_avg'] < 1].count()


# In[21]:


bots = finalmerge[finalmerge['variance_of_timestamp_diff_avg'] < 1]
bots


# In[22]:


bots['count'].sum()


# In[23]:


bots['count'].mean()


# In[24]:


bots['count'].min()


# In[ ]:


# create barplot with counts of "bots"


# In[25]:


import pandas as pd

usernames_array = bots['user'].to_numpy()
len(usernames_array)


# In[26]:


username_list = usernames_array.tolist()


# In[27]:


import polars as pl
import boto3
from io import BytesIO

# Specify the S3 URI
s3_uri = 's3://rplace-data-naj/Combined_parquets/combined_chunk_0.parquet'

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


# In[28]:


day1bots = df.filter(pl.col('user').is_in(username_list))
day1bots


# In[30]:


# Specify the S3 URI
s3_uri = 's3://rplace-data-naj/Combined_parquets/combined_chunk_1.parquet'

# Split the S3 URI into bucket and key
bucket, key = s3_uri.replace('s3://', '').split('/', 1)

# Accessing the S3 bucket
s3 = boto3.client('s3')

# Read the Parquet file from S3 into a DataFrame
with BytesIO() as f:
    s3.download_fileobj(bucket, key, f)
    f.seek(0)
    df2 = pl.read_parquet(f)

# Display the first few rows of the DataFrame
df2.head()


# In[31]:


day2bots = df2.filter(pl.col('user').is_in(username_list))
day2bots


# In[32]:


# Specify the S3 URI
s3_uri = 's3://rplace-data-naj/Combined_parquets/combined_chunk_2.parquet'

# Split the S3 URI into bucket and key
bucket, key = s3_uri.replace('s3://', '').split('/', 1)

# Accessing the S3 bucket
s3 = boto3.client('s3')

# Read the Parquet file from S3 into a DataFrame
with BytesIO() as f:
    s3.download_fileobj(bucket, key, f)
    f.seek(0)
    df3 = pl.read_parquet(f)

# Display the first few rows of the DataFrame
df3.head()
day3bots = df3.filter(pl.col('user').is_in(username_list))
day3bots


# In[33]:


# Specify the S3 URI
s3_uri = 's3://rplace-data-naj/Combined_parquets/combined_chunk_3.parquet'

# Split the S3 URI into bucket and key
bucket, key = s3_uri.replace('s3://', '').split('/', 1)

# Accessing the S3 bucket
s3 = boto3.client('s3')

# Read the Parquet file from S3 into a DataFrame
with BytesIO() as f:
    s3.download_fileobj(bucket, key, f)
    f.seek(0)
    df4 = pl.read_parquet(f)

# Display the first few rows of the DataFrame
df4.head()
day4bots = df4.filter(pl.col('user').is_in(username_list))
day4bots


# In[34]:


# Specify the S3 URI
s3_uri = 's3://rplace-data-naj/Combined_parquets/combined_chunk_4.parquet'

# Split the S3 URI into bucket and key
bucket, key = s3_uri.replace('s3://', '').split('/', 1)

# Accessing the S3 bucket
s3 = boto3.client('s3')

# Read the Parquet file from S3 into a DataFrame
with BytesIO() as f:
    s3.download_fileobj(bucket, key, f)
    f.seek(0)
    df5 = pl.read_parquet(f)

# Display the first few rows of the DataFrame
df5.head()
day5bots = df5.filter(pl.col('user').is_in(username_list))
day5bots


# In[35]:


# Specify the S3 URI
s3_uri = 's3://rplace-data-naj/Combined_parquets/combined_chunk_5.parquet'

# Split the S3 URI into bucket and key
bucket, key = s3_uri.replace('s3://', '').split('/', 1)

# Accessing the S3 bucket
s3 = boto3.client('s3')

# Read the Parquet file from S3 into a DataFrame
with BytesIO() as f:
    s3.download_fileobj(bucket, key, f)
    f.seek(0)
    df6 = pl.read_parquet(f)

# Display the first few rows of the DataFrame
df6.head()
day6bots = df6.filter(pl.col('user').is_in(username_list))
day6bots


# In[36]:


dfbots_activity = pl.concat([day1bots, day2bots, day3bots, day4bots, day5bots, day6bots])
dfbots_activity


# In[37]:


bot_activity_pd = dfbots_activity.to_pandas()
bot_activity_pd


# In[38]:


bot_activity_pd['timestamp_new'] = pd.to_datetime(bot_activity_pd['timestamp'])

# Resample or group by day and count the number of activities.

daily_activity = bot_activity_pd.resample('H', on='timestamp_new').size().reset_index(name='count')


plot = (ggplot(daily_activity, aes(x='timestamp_new', y='count')) +
        geom_line() +
        labs(title='Bot Activity Over Time', x='Timestamp', y='Activity Count'))


# In[40]:


bot_activity_pd['timestamp'] = pd.to_datetime(bot_activity_pd['timestamp'], infer_datetime_format=True)

# Resample or group by day and count the number of activities.
daily_activity = bot_activity_pd.groupby(bot_activity_pd['timestamp'].dt.date).size().reset_index(name='count')
daily_activity['timestamp'] = pd.to_datetime(daily_activity['timestamp'])

# Plot the line plot with plotnine.
plot = (ggplot(daily_activity, aes(x='timestamp', y='count')) +
        geom_line() +
        labs(title='Bot Activity Over Time', x='Timestamp', y='Activity Count'))

# Display the plot.
print(plot)


# In[41]:


dfbots_activity = dfbots_activity.with_columns(pl.col("timestamp").str.slice(11, 2).alias("hour"),
               pl.col("timestamp").str.slice(14, 2).alias("minute"),
               pl.col("timestamp").str.slice(17, 2).alias("second"))
dfbots_activity = dfbots_activity.with_columns(pl.col("hour").cast(pl.Int64),
               pl.col("minute").cast(pl.Int64),
               pl.col('second').cast(pl.Int64))
dfbots_activity = dfbots_activity.with_columns(((pl.col("hour")*3600) + (pl.col("minute")*60) + pl.col('second')).alias("second_in_day"))
dfbots_activity.head()


# In[120]:


user_activity_counts = dfbots_activity.groupby('user').count().sort(by='count', descending = False)
pd_user_activity_counts= user_activity_counts.to_pandas()
pd_user_activity_counts


# In[126]:


# import numpy as np
# pd_user_activity_counts['bins'] = pd.cut(np.array([1,5, 10]),
#        3, labels=["bad", "medium", "good"])

bins = [0, 5, 30, 50, np.inf]
names = ['0-5', '5-30', '30-50', '50+']

pd_user_activity_counts['bins'] = pd.cut(pd_user_activity_counts['count'], bins, labels=names)
pd_user_activity_counts.head()


# In[131]:


plot = (
    ggplot(pd_user_activity_counts) +
    aes(x='bins') +
    geom_bar(fill='skyblue') +  # Plot the count of users in each bin
    theme_minimal() +
    labs(title='User Activity Distribution', x='Activity Count Bin', y='Number of Users')
)

plot.draw()


# In[122]:


import pandas as pd
from plotnine import ggplot, aes, geom_bar, labs, theme_minimal


# Aggregate user activities, assuming 'activity' is a column you can count, or simply count rows
user_activity_counts = pd_user_activity_counts.groupby('user').size().reset_index(name='count')

# Create bins for activity count
user_activity_counts['activity_bin'] = pd.cut(
    user_activity_counts['count'],
    bins=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, float('inf')],  # Define bin edges
    labels=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10+'],  # Define bin labels
    include_lowest=True,
    right=False
)

# Ensure the activity_bin column is of type 'category' for proper plotnine handling
user_activity_counts['activity_bin'] = user_activity_counts['activity_bin'].astype('category')

# Plotting with plotnine
plot = (
    ggplot(user_activity_counts) +
    aes(x='activity_bin') +
    geom_bar(fill='skyblue') +  # Plot the count of users in each bin
    theme_minimal() +
    labs(title='User Activity Distribution', x='Activity Count Bin', y='Number of Users')
)

plot.draw()


# In[104]:


#!pip install plotnine
from plotnine import *




# In[101]:


dfbots_activity.write_parquet('bots_active.parquet')
import boto3


s3_client = boto3.client('s3')

# Specify your bucket name and the key (file path within the bucket)
bucket_name = 'rplace-data-naj'
object_key = 'Diff_in_variance/bots_active.parquet'

# Upload the file
with open('bots_active.parquet', 'rb') as f:
    s3_client.upload_fileobj(f, bucket_name, object_key)
    

