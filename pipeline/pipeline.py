import sys
import pandas as pd

print("argument:", sys.argv)
month=int(sys.argv[1])
df=pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
df['month']=month
print(df.head())
df.to_parquet(f"output_{month}.parquet", index=False)


print(f"hello pipeline, month={month}")