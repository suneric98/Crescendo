import json
import pandas as pd

df = pd.read_csv('topChartWithFeatures.csv')
print(df.shape)
numDays = {}
for idx,row in df.iterrows():
    # key = row["Song"] + "/:/" + row["Artist"]
    key = row["Artist"]
    numDays[key] = numDays.get(key, 0) + 1

rowsToRemove = []
for idx, row in df.iterrows():
    # key = row["Song"] + "/:/" + row["Artist"]
    key = row["Artist"]
    if numDays[key] < 300:
        rowsToRemove.append(idx)

df = df.drop(rowsToRemove)

print(df.shape)

df.to_csv("line_vis_data.csv", index=False)