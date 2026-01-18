import numpy as np
import pandas as pd

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('jp_vs_cn.csv')

# Convert the DataFrame to a NumPy array
data = df.to_numpy()

# Print basic information
print("Shape of the data:", data.shape)
print("Data types:\n", df.dtypes)
print("Summary of the data:\n", df.describe())

#print out the first 10 rows of data whose likes are biggest and show the Comment column

print(df.nlargest(10, 'Likes')['Comment'])