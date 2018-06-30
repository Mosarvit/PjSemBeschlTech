#! /usr/bin/env python
import pandas as pd
import sys

df = pd.DataFrame([[1, 2], [3, 4]], columns=['A','B'])

# get count of header columns, add REAL for each one
types_header_for_insert = list(df.columns.values)
for idx, val in enumerate(types_header_for_insert):
    types_header_for_insert[idx] = ' '


# count number of index columns, then add STRING for each one
index_count = len(df.index.names)
for idx in range(0, index_count):
    df.reset_index(level=0, inplace=True)
    types_header_for_insert.insert(0, ' ')

types_header_for_insert = [' ','t/s','y/V']
# insert the new types column
#df.columns = pd.MultiIndex.from_tuples(zip(df.columns, types_header_for_insert))

#set new value to dataframe
df.loc[-1]  = types_header_for_insert
df.loc[-2]  = [' ',' ',' ']
df.loc[-3]  = [' ',' ',' ']
df.loc[-4]  = [' ',' ',' ']
#sort index
df = df.sort_index()
df.to_csv('Hi.csv',index=False,header = False)
"""
#empty df with column from df
df1 = pd.DataFrame(columns = df.columns)
#create series from types_header_for_insert
s = pd.Series(types_header_for_insert, index=df.columns)

df1 = df1.append(s, ignore_index=True).append(df, ignore_index=True)

print (df1.to_csv(index=False))
df1.to_csv('Hi.csv',index=False)
sys.exit()
"""
