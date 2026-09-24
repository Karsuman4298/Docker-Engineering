#!/usr/bin/env python
# coding: utf-8



import pandas as pd
from tqdm.auto import tqdm
from sqlalchemy import create_engine
import pandas as pd
year=2021
month=1

pg_user="root"
pg_pass="root"
pg_host="localhost"
pg_port="5432"
pg_db="ny_taxi"
chunksize=100000

pd.__file__


# Read a sample of the data
prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
df = pd.read_csv(prefix + 'yellow_tripdata_2021-01.csv.gz')

# Display first rows
df.head()

# Check data types
df.dtypes

# Check data shape
df.shape


# In[7]:


df.head()


# In[12]:


x=df.shape[0]


# In[13]:


y=df["VendorID"].count()


# In[17]:


missing_vid=x-y
missing_vid


# In[18]:


dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

df = pd.read_csv(
    prefix + 'yellow_tripdata_2021-01.csv.gz',
    nrows=100,
    dtype=dtype,
    parse_dates=parse_dates
)


# In[19]:


df.head()


# In[20]:


get_ipython().system('uv add sqlalchemy "psycopg[binary,pool]"')


engine = create_engine(f'postgresql+psycopg://root:root@{pg_host}:{pg_port}/{pg_db}')


# In[23]:


print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))


# In[24]:


df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')


# In[25]:


df_iter = pd.read_csv(
    prefix + 'yellow_tripdata_2021-01.csv.gz',
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,
    chunksize=100000
)   


# In[26]:


get_ipython().system('uv add tqdm')


# In[27]:



first = True

for df_chunk in tqdm(df_iter):

    if first:
        # Create table schema (no data)
        df_chunk.head(0).to_sql(
            name="yellow_taxi_data",
            con=engine,
            if_exists="replace"
        )
        first = False
        print("Table created")

    # Insert chunk
    df_chunk.to_sql(
        name="yellow_taxi_data",
        con=engine,
        if_exists="append"
    )

    print("Inserted:", len(df_chunk))


# In[ ]:




