#import wbgapi as wb   # I use wb as a namespace in all my work
import pandas as pd   # optional but highly recommended for wbgapi
import matplotlib.pyplot as plt

%matplotlib inline

# Missing values
df['ECA'] = df['ECA'].fillna(0)
df.reset_index(inplace=True)

# Recode based on the specified intervals
df['date'] = pd.cut(df['date'], [1980, 1989, 2002, 2013, 2019, 2021], labels=[1, 2, 3, 4, 5])

# Define labels for 'date'
date_labels = {1: "1980-1989", 2: "1990-2002", 3: "2003-2013", 4: "2014-2019", 5: "2020-2021"}
df['date'] = df['date'].map(date_labels)

# Collapse the data by 'date' and calculate the mean of 'EAP', 'ECA', 'LCN', and 'WLD'
collapsed_data = df.groupby('date').agg({'EAP': 'mean', 'ECA': 'mean', 'LCN': 'mean', 'WLD': 'mean'}).reset_index()

# Plot the grouped bar graph
width = 0.2
date_values = collapsed_data['date'].unique()
x = range(len(date_values))

plt.figure(figsize=(10, 6))
plt.bar(x, collapsed_data['LCN'], width=width, label="LAC")
plt.bar([i + width for i in x], collapsed_data['EAP'], width=width, label="EAP")
plt.bar([i + 2 * width for i in x], collapsed_data['WLD'], width=width, label="World")
plt.bar([i + 3 * width for i in x], collapsed_data['ECA'], width=width, label="ECA")

plt.xlabel("")
plt.ylabel("Title y axis")
plt.title("Title")
plt.xticks([i + 1.5 * width for i in x], date_values)
plt.legend()
plt.show()
