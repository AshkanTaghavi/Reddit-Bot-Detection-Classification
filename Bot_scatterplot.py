#!/usr/bin/env python
# coding: utf-8

# ### Loading in the first chunk

# In[1]:


import pandas as pd

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
    df = pd.read_parquet(f)

# Display the first few rows of the DataFrame
df.head()


# In[2]:


# Counting how many pixels each user placed
user_pixel_counts = df.groupby('user').size().reset_index(name = 'pixel_count')

# Display top ten user counts
user_pixel_counts.sort_values(by='pixel_count', ascending=False).head()


# ### Running the Function for Variance

# In[34]:


import pandas as pd
import boto3
from io import BytesIO
import s3fs

def clean_and_convert_coordinate(coord):
    # Extract numerical parts from the coordinate string
    parts = coord.split(',')
    x_coord = int(parts[0].split(':')[-1].strip())
    y_coord = int(parts[1].split(':')[-1].strip())
    return x_coord, y_coord

def calculate_variance(chunk):
    # Clean and convert coordinate column
    chunk['x_coordinate'], chunk['y_coordinate'] = zip(*chunk['coordinate'].apply(clean_and_convert_coordinate))
    
    # Calculate variance of x and y coordinates grouped by user
    variance_by_user = chunk.groupby('user')[['x_coordinate', 'y_coordinate']].var()
    return variance_by_user

def process_chunk_and_store_result(chunk, output_bucket, output_key):
    # Perform variance calculation on the chunk
    variance_results = calculate_variance(chunk)
    
    # Store variance results back to S3
    with BytesIO() as f:
        variance_results.to_parquet(f)
        f.seek(0)
        s3 = boto3.client('s3')
        s3.upload_fileobj(f, output_bucket, output_key)

def process_all_chunks(input_bucket, input_prefix, output_bucket, output_prefix, chunk_size=100000):
    s3 = s3fs.S3FileSystem()
    
    # Get list of files in the input bucket with the specified prefix
    files = s3.glob(f'{input_bucket}/{input_prefix}/*.parquet')
    
    # Process each file
    for file in files:
        # Read Parquet file
        with s3.open(file, 'rb') as f:
            # Read Parquet file directly into DataFrame
            chunk_df = pd.read_parquet(f)
        
        # Process the chunk and store the result
        output_key = f"{output_prefix}/{file.split('/')[-1].split('.')[0]}_variance.parquet"
        process_chunk_and_store_result(chunk_df, output_bucket, output_key)

# Example usage
input_bucket = 'rplace-data-naj'
input_prefix = 'Combined_parquets'
output_bucket = 'rplace-data-naj'
output_prefix = 'Variance_analysis'
process_all_chunks(input_bucket, input_prefix, output_bucket, output_prefix)


# ### Loading in Variance Chunks

# In[3]:


import pandas as pd

# Importing Boto3 library to access AWS resources
import boto3
from io import BytesIO

# Specify the S3 URI
s3_uri = 's3://rplace-data-naj/Variance_analysis/combined_chunk_0_variance.parquet'

# Split the S3 URI into bucket and key
bucket, key = s3_uri.replace('s3://', '').split('/', 1)

# Accessing the S3 bucket
s3 = boto3.client('s3')

# Read the Parquet file from S3 into a DataFrame
with BytesIO() as f:
    s3.download_fileobj(bucket, key, f)
    f.seek(0)
    df_var = pd.read_parquet(f)

# Display the first few rows of the DataFrame
df_var.head()


# In[5]:


# Drop NA values
df_clean = df_var.dropna()
df_clean['total_coordinates'] = df_clean[['x_coordinate', 'y_coordinate']].sum(axis=1)
df_sorted = df_clean.sort_values(by='total_coordinates', ascending=True)

df_sorted.head()


# ### Attempting to plot

# In[6]:


import pandas as pd

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
    df = pd.read_parquet(f)

# Display the first few rows of the DataFrame
df.head()


# In[7]:


# Remove the timestamp and user for the time being
df_new = df.drop(['timestamp', 'user', 'coordinate'], axis=1)
df.head()


# In[9]:


# Visualizing only bots
import pandas as pd

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
    df_bots = pd.read_parquet(f)

# Display the first few rows of the DataFrame
df_bots.head()


# In[10]:


# Rearranging Coordinates
def clean_and_convert_coordinate(coord):
    # Extract numerical parts from the coordinate string
    parts = coord.split(',')
    x_coord = int(parts[0].split(':')[-1].strip())
    y_coord = int(parts[1].split(':')[-1].strip())
    return x_coord, y_coord

df_bots['x_coordinate'], df_bots['y_coordinate'] = zip(*df_bots['coordinate'].apply(clean_and_convert_coordinate))
df_bots.head()


# In[11]:


import matplotlib.pyplot as plt

# Plotting bots only
plt.figure(figsize=(12, 9))
plt.scatter(df_bots['x_coordinate'], df_bots['y_coordinate'], c=df_bots['pixel_color'], marker='s', s=1)

# Customize the plot
plt.title('Pixel Colors at Coordinates')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.grid(False)

# Hide the colorbar legend
plt.colorbar(label='Pixel Color').remove()

# Set the background color of the plot area to black
plt.gca().set_facecolor('black')

# Show the plot
plt.show()

