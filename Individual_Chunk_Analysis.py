#!/usr/bin/env python
# coding: utf-8

# In[225]:


import polars as pl

# Importing Boto3 library to access AWS resources
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


# In[226]:


# Make each DateTime as YYYY-MM-DD HH:MM:SS
df = df.with_columns(pl.col("timestamp").str.slice(0, 19).alias("clean_timestamp"))


# In[227]:


# Make 'clean_timestamp' to datetime object
df = df.with_columns([
    pl.col("clean_timestamp").str.to_datetime("%Y-%m-%d %H:%M:%S")
])


# In[122]:


df['clean_timestamp'][0] # Example of clean_timestamp


# In[228]:


df = df.with_columns(pl.col("timestamp").str.slice(8, 2).alias("day")) # Extract Date


# In[124]:


df.head()


# In[125]:


df['day'].unique() # First parquet chunk encompases 20th and 21st


# In[229]:


# Count number of clicks per user by day
day1 = df.groupby(['user', 'day']).agg(pl.count('coordinate').alias('count'))


# In[127]:


day1 = day1.filter(pl.col('day') == '20') # Keep only 20th


# In[218]:


usercount20 = day1.sort('count', descending = True)
usercount20


# In[129]:


df['timestamp'][0]


# In[130]:


df = df.with_columns(pl.col("timestamp").str.slice(11, 2).alias("hour"),
               pl.col("timestamp").str.slice(14, 2).alias("minute"),
               pl.col("timestamp").str.slice(17, 2).alias("second")) # Extract Date


# In[131]:


# Make hour, minute, second into Integers
df = df.with_columns(pl.col("hour").cast(pl.Int64),
               pl.col("minute").cast(pl.Int64),
               pl.col('second').cast(pl.Int64))


# In[132]:


# Calculate Second in Day Metric
df = df.with_columns(((pl.col("hour")*3600) + (pl.col("minute")*60) + pl.col('second')).alias("second_in_day"))
df.head()


# In[133]:


the20th = df.filter(pl.col('day') == '20')
the20th.head()


# In[134]:


#the20th.groupby('user').agg(pl.difference('second_in_day').alias('test'))
the20th.groupby('user').agg((pl.col("second_in_day") - pl.col("second_in_day").mean()).mean().alias('mean_diff_second_in_day'))




# In[136]:


uservariance20 = the20th.groupby('user').agg(pl.var('second_in_day').alias('user_variance'))
uservariance20 = uservariance20.drop_nulls()
uservariance20.sort('user_variance', descending = True)


# In[137]:


joined = usercount20.join(uservariance20, left_on="user", right_on="user")
joined


# In[138]:


joined.filter((pl.col("count") >= 5) & (pl.col("count") < 288)).sort('user_variance', descending = False)


# In[140]:


df.head()


# In[ ]:





# In[17]:


import polars as pl

def calculate_user_variance_of_differences(df, user_col='user', timestamp_col='second_in_day'):
    """
    Calculate the variance of timestamp differences for each user in a Polars DataFrame.
    
    Parameters:
    - df: Polars DataFrame containing the data.
    - user_col: Column name for the user identifier.
    - timestamp_col: Column name for the timestamp in seconds.
    
    Returns:
    - A Polars DataFrame with users and their variance of timestamp differences.
    """
    # Ensure the DataFrame is sorted by user and timestamp for correct diff calculation
    df = df.sort([user_col, timestamp_col])
    
    # Calculate the difference in timestamps for each user
    df = df.with_columns(
        pl.col(timestamp_col).diff().over(user_col).alias('timestamp_diff')
    )
    
    # Compute the variance of these differences for each user
    user_variance = df.groupby(user_col).agg(
        pl.var('timestamp_diff').alias('variance_of_timestamp_diff')
    ).filter(pl.col('variance_of_timestamp_diff').is_not_null())
    
    # Return the DataFrame with user variance
    return user_variance

# Example usage:
# Assuming `df` is your Polars DataFrame with 'user' and 'second_in_day' columns
# df = the20th  # or however you obtain your DataFrame
# user_variance_df = calculate_user_variance_of_differences(df)
# print(user_variance_df)


# In[168]:


df = the20th  
user_variance_df = calculate_user_variance_of_differences(df)
user_variance_df


# In[185]:


df = the20th.sort(['user', 'timestamp'])
user_variance_df = calculate_user_variance_of_differences(df)
sorted_df_var = user_variance_df.sort(by = 'variance_of_timestamp_diff', descending = True)
sorted_df_var


# In[186]:


# Assuming user_variance_df is your Polars DataFrame and 'user' is the column with usernames
first_user_name = sorted_df_var.select('user').row(0)[0]  # Select 'user' column and get the first value

print(first_user_name)



# In[187]:


df.filter((pl.col('user')=='GgCMfQ/LqDKFD0WqLjcut0ciO8LP+NrtWJNlVnUHcokj9ORyqsMhJOlOJxw8ftYozklLKkQv3UoT1sKkhxBMgg=='))


# In[189]:


import numpy as np
num = [47543, 85899, 86282]
differences2 = np.diff(num)
np.var(differences2, ddof=1)


# In[ ]:


usercount20 = day1.sort('count', descending = True)
usercount20.head()


# In[212]:


joined2 = usercount20.join(sorted_df_var, left_on="user", right_on="user")
day1var = joined2.sort(by = 'variance_of_timestamp_diff', descending = True)
day1var


# In[214]:


joined2.filter((pl.col('count') > 4) & 
               (pl.col('count') < 288)).sort(
    by = 'variance_of_timestamp_diff', descending = False)


# In[221]:


day1var.write_parquet('day1var.parquet')
import boto3


s3_client = boto3.client('s3')

# Specify your bucket name and the key (file path within the bucket)
bucket_name = 'rplace-data-naj'
object_key = 'Diff_in_variance/day1var.parquet'

# Upload the file
with open('day1var.parquet', 'rb') as f:
    s3_client.upload_fileobj(f, bucket_name, object_key)


# # Day 2

# In[230]:


df.head()


# In[231]:


day2 = df.groupby(['user', 'day']).agg(pl.count('coordinate').alias('count'))


# In[232]:


day2


# In[233]:


df = df.with_columns(pl.col("timestamp").str.slice(11, 2).alias("hour"),
               pl.col("timestamp").str.slice(14, 2).alias("minute"),
               pl.col("timestamp").str.slice(17, 2).alias("second")) # Extract Date


# In[234]:


# Make hour, minute, second into Integers
df = df.with_columns(pl.col("hour").cast(pl.Int64),
               pl.col("minute").cast(pl.Int64),
               pl.col('second').cast(pl.Int64))


# In[235]:


# Calculate Second in Day Metric
df = df.with_columns(((pl.col("hour")*3600) + (pl.col("minute")*60) + pl.col('second')).alias("second_in_day"))
df.head()


# In[238]:


the21st = df.filter(pl.col('day') == '21')
the21st.head()


# In[2]:


import polars as pl

# # Importing Boto3 library to access AWS resources
import boto3
from io import BytesIO

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


# In[3]:


# Make each DateTime as YYYY-MM-DD HH:MM:SS
df2 = df2.with_columns(pl.col("timestamp").str.slice(0, 19).alias("clean_timestamp"))


# In[4]:


# Make 'clean_timestamp' to datetime object
df2 = df2.with_columns([
    pl.col("clean_timestamp").str.to_datetime("%Y-%m-%d %H:%M:%S")
])


# In[5]:


df2 = df2.with_columns(pl.col("timestamp").str.slice(8, 2).alias("day")) # Extract Date


# In[6]:


df2 = df2.with_columns(pl.col("timestamp").str.slice(11, 2).alias("hour"),
               pl.col("timestamp").str.slice(14, 2).alias("minute"),
               pl.col("timestamp").str.slice(17, 2).alias("second")) # Extract Date


# In[7]:


# Make hour, minute, second into Integers
df2 = df2.with_columns(pl.col("hour").cast(pl.Int64),
               pl.col("minute").cast(pl.Int64),
               pl.col('second').cast(pl.Int64))


# In[8]:


# Calculate Second in Day Metric
df2 = df2.with_columns(((pl.col("hour")*3600) + (pl.col("minute")*60) + pl.col('second')).alias("second_in_day"))
df2.head()


# In[9]:


the21stPART2 = df2.filter(pl.col('day') == '21')
the21stPART2.head()


# In[267]:


the21stPART2.head()


# In[248]:


the21st.head()


# In[269]:


#the21st.hstack(the21stPART2)
dfd2 = pl.concat([the21st, the21stPART2])
dfd2.head()


# In[272]:


day2counts = dfd2.groupby(['user', 'day']).agg(pl.count('coordinate').alias('count'))
day2counts.sort('count', descending = True).head()


# In[273]:


user_variance_dfd2 = calculate_user_variance_of_differences(dfd2)
user_variance_dfd2


# In[277]:


joined2 = day2counts.join(user_variance_dfd2, left_on='user', right_on = 'user')
joined2.sort('variance_of_timestamp_diff', descending = False)


# In[287]:


day2var.head()


# In[288]:


day2var = joined2
day2var.write_parquet('day2var.parquet')
import boto3


s3_client = boto3.client('s3')

# Specify your bucket name and the key (file path within the bucket)
bucket_name = 'rplace-data-naj'
object_key = 'Diff_in_variance/day2var.parquet'

# Upload the file
with open('day2var.parquet', 'rb') as f:
    s3_client.upload_fileobj(f, bucket_name, object_key)


# # Day 3

# In[10]:


the22nd = df2.filter(pl.col('day') == '22')
the22nd.head()


# In[11]:


# import polars as pl

# # Importing Boto3 library to access AWS resources
# import boto3
# from io import BytesIO

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


# In[12]:


# Make each DateTime as YYYY-MM-DD HH:MM:SS
df3 = df3.with_columns(pl.col("timestamp").str.slice(0, 19).alias("clean_timestamp"))

# Make 'clean_timestamp' to datetime object
df3 = df3.with_columns([
    pl.col("clean_timestamp").str.to_datetime("%Y-%m-%d %H:%M:%S")
])

df3 = df3.with_columns(pl.col("timestamp").str.slice(8, 2).alias("day")) # Extract Date

df3 = df3.with_columns(pl.col("timestamp").str.slice(11, 2).alias("hour"),
               pl.col("timestamp").str.slice(14, 2).alias("minute"),
               pl.col("timestamp").str.slice(17, 2).alias("second")) # Extract Date

# Make hour, minute, second into Integers
df3 = df3.with_columns(pl.col("hour").cast(pl.Int64),
               pl.col("minute").cast(pl.Int64),
               pl.col('second').cast(pl.Int64))

# Calculate Second in Day Metric
df3 = df3.with_columns(((pl.col("hour")*3600) + (pl.col("minute")*60) + pl.col('second')).alias("second_in_day"))
df3.head()


# In[13]:


the22ndPART2 = df3.filter(pl.col('day') == '22')
the22ndPART2.head()


# In[14]:


#the21st.hstack(the21stPART2)
dfd3 = pl.concat([the22nd, the22ndPART2])
dfd3.head()


# In[15]:


day3counts = dfd3.groupby(['user', 'day']).agg(pl.count('coordinate').alias('count'))
day3counts.sort('count', descending = True).head()


# In[18]:


user_variance_dfd3 = calculate_user_variance_of_differences(dfd3)
user_variance_dfd3


# In[19]:


joined3 = day3counts.join(user_variance_dfd3, left_on='user', right_on = 'user')
joined3.sort('variance_of_timestamp_diff', descending = False)


# In[20]:


day3var = joined3
day3var.write_parquet('day3var.parquet')
import boto3


s3_client = boto3.client('s3')

# Specify your bucket name and the key (file path within the bucket)
bucket_name = 'rplace-data-naj'
object_key = 'Diff_in_variance/day3var.parquet'

# Upload the file
with open('day3var.parquet', 'rb') as f:
    s3_client.upload_fileobj(f, bucket_name, object_key)


# # DAY 3 (23rd)

# In[26]:


the23rd = df3.filter(pl.col('day') == '23')
the23rd.head()


# In[22]:


# import polars as pl

# # Importing Boto3 library to access AWS resources
# import boto3
# from io import BytesIO

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


# In[23]:


# Make each DateTime as YYYY-MM-DD HH:MM:SS
df4 = df4.with_columns(pl.col("timestamp").str.slice(0, 19).alias("clean_timestamp"))

# Make 'clean_timestamp' to datetime object
df4 = df4.with_columns([
    pl.col("clean_timestamp").str.to_datetime("%Y-%m-%d %H:%M:%S")
])

df4 = df4.with_columns(pl.col("timestamp").str.slice(8, 2).alias("day")) # Extract Date

df4 = df4.with_columns(pl.col("timestamp").str.slice(11, 2).alias("hour"),
               pl.col("timestamp").str.slice(14, 2).alias("minute"),
               pl.col("timestamp").str.slice(17, 2).alias("second")) # Extract Date

# Make hour, minute, second into Integers
df4 = df4.with_columns(pl.col("hour").cast(pl.Int64),
               pl.col("minute").cast(pl.Int64),
               pl.col('second').cast(pl.Int64))

# Calculate Second in Day Metric
df4 = df4.with_columns(((pl.col("hour")*3600) + (pl.col("minute")*60) + pl.col('second')).alias("second_in_day"))
df4.head()


# In[24]:


the23rdPART2 = df4.filter(pl.col('day') == '23')
the23rdPART2.head()


# In[27]:


#the21st.hstack(the21stPART2)
dfd4 = pl.concat([the23rd, the23rdPART2])
dfd4.head()


# In[28]:


day4counts = dfd4.groupby(['user', 'day']).agg(pl.count('coordinate').alias('count'))
day4counts.sort('count', descending = True).head()


# In[29]:


user_variance_dfd4 = calculate_user_variance_of_differences(dfd4)
user_variance_dfd4


# In[30]:


joined4 = day4counts.join(user_variance_dfd4, left_on='user', right_on = 'user')
joined4.sort('variance_of_timestamp_diff', descending = False)


# In[31]:


day4var = joined4
day4var.write_parquet('day4var.parquet')
import boto3


s3_client = boto3.client('s3')

# Specify your bucket name and the key (file path within the bucket)
bucket_name = 'rplace-data-naj'
object_key = 'Diff_in_variance/day4var.parquet'

# Upload the file
with open('day4var.parquet', 'rb') as f:
    s3_client.upload_fileobj(f, bucket_name, object_key)


# # Day 4 (24th)

# In[32]:


the24th = df4.filter(pl.col('day') == '24')
the24th.head()


# In[34]:


# import polars as pl

# # Importing Boto3 library to access AWS resources
# import boto3
# from io import BytesIO

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


# In[35]:


# Make each DateTime as YYYY-MM-DD HH:MM:SS
df5 = df5.with_columns(pl.col("timestamp").str.slice(0, 19).alias("clean_timestamp"))

# Make 'clean_timestamp' to datetime object
df5 = df5.with_columns([
    pl.col("clean_timestamp").str.to_datetime("%Y-%m-%d %H:%M:%S")
])

df5 = df5.with_columns(pl.col("timestamp").str.slice(8, 2).alias("day")) # Extract Date

df5 = df5.with_columns(pl.col("timestamp").str.slice(11, 2).alias("hour"),
               pl.col("timestamp").str.slice(14, 2).alias("minute"),
               pl.col("timestamp").str.slice(17, 2).alias("second")) # Extract Date

# Make hour, minute, second into Integers
df5 = df5.with_columns(pl.col("hour").cast(pl.Int64),
               pl.col("minute").cast(pl.Int64),
               pl.col('second').cast(pl.Int64))

# Calculate Second in Day Metric
df5 = df5.with_columns(((pl.col("hour")*3600) + (pl.col("minute")*60) + pl.col('second')).alias("second_in_day"))
df5.head()


# In[36]:


the24thPART2 = df5.filter(pl.col('day') == '24')
the24thPART2.head()


# In[37]:


#the21st.hstack(the21stPART2)
dfd5 = pl.concat([the24th, the24thPART2])
dfd5.head()


# In[38]:


day5counts = dfd5.groupby(['user', 'day']).agg(pl.count('coordinate').alias('count'))
day5counts.sort('count', descending = True).head()


# In[39]:


user_variance_dfd5 = calculate_user_variance_of_differences(dfd5)
user_variance_dfd5


# In[40]:


joined5 = day5counts.join(user_variance_dfd5, left_on='user', right_on = 'user')
joined5.sort('variance_of_timestamp_diff', descending = False)


# In[41]:


day5var = joined5
day5var.write_parquet('day5var.parquet')
import boto3


s3_client = boto3.client('s3')

# Specify your bucket name and the key (file path within the bucket)
bucket_name = 'rplace-data-naj'
object_key = 'Diff_in_variance/day5var.parquet'

# Upload the file
with open('day5var.parquet', 'rb') as f:
    s3_client.upload_fileobj(f, bucket_name, object_key)


# # Day 5 (25th)

# In[47]:


dfd5['day'].unique()


# In[46]:


# import polars as pl

# # Importing Boto3 library to access AWS resources
# import boto3
# from io import BytesIO

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


# In[48]:


# Make each DateTime as YYYY-MM-DD HH:MM:SS
df6 = df6.with_columns(pl.col("timestamp").str.slice(0, 19).alias("clean_timestamp"))

# Make 'clean_timestamp' to datetime object
df6 = df6.with_columns([
    pl.col("clean_timestamp").str.to_datetime("%Y-%m-%d %H:%M:%S")
])

df6 = df6.with_columns(pl.col("timestamp").str.slice(8, 2).alias("day")) # Extract Date

df6 = df6.with_columns(pl.col("timestamp").str.slice(11, 2).alias("hour"),
               pl.col("timestamp").str.slice(14, 2).alias("minute"),
               pl.col("timestamp").str.slice(17, 2).alias("second")) # Extract Date

# Make hour, minute, second into Integers
df6 = df6.with_columns(pl.col("hour").cast(pl.Int64),
               pl.col("minute").cast(pl.Int64),
               pl.col('second').cast(pl.Int64))

# Calculate Second in Day Metric
df6 = df6.with_columns(((pl.col("hour")*3600) + (pl.col("minute")*60) + pl.col('second')).alias("second_in_day"))
df6.head()


# In[50]:


dfd6 = df6
day6counts = dfd6.groupby(['user', 'day']).agg(pl.count('coordinate').alias('count'))
day6counts.sort('count', descending = True).head()


# In[51]:


user_variance_dfd6 = calculate_user_variance_of_differences(dfd6)
user_variance_dfd6


# In[52]:


joined6 = day6counts.join(user_variance_dfd6, left_on='user', right_on = 'user')
joined6.sort('variance_of_timestamp_diff', descending = False)


# In[53]:


day6var = joined6
day6var.write_parquet('day6var.parquet')
import boto3


s3_client = boto3.client('s3')

# Specify your bucket name and the key (file path within the bucket)
bucket_name = 'rplace-data-naj'
object_key = 'Diff_in_variance/day6var.parquet'

# Upload the file
with open('day6var.parquet', 'rb') as f:
    s3_client.upload_fileobj(f, bucket_name, object_key)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




