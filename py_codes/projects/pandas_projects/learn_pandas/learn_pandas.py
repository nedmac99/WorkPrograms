import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


file_path = Path(__file__).parent / "units.csv"

#Creating a Series data set(1 Dimensional)

s_data = [10, 20, 30]
series = pd.Series(s_data)
#print(series)


#Creating a Data Frame(2 Dimensioinal)

df_data = {
    'Name': ["Alice", "Bob", "Charlie"],
    'Age': [25, 30, 35] 
}
df = pd.DataFrame(df_data)
print(f"Before cleaning: \n{df}\n")


#Loading Real Data from O2 Inventory
'''
file_path = Path(__file__).parent / "units.csv"
df = pd.read_csv(file_path)
print(f"First 5 entries: \n{df.head()}\n")
print(f"{df.info()}\n")
print(f"Description of stats: \n{df.describe()}\n")
print(f"Column names: \n{df.columns}\n")
print(f"\nRows, Columns: \n{df.shape}\n")

#Common Methods
df.info()        # Overview: columns, types, missing values
df.describe()    # Summary statistics for numeric columns
df.columns       # List column names
df.shape         # (rows, columns)
'''

#Accessing Data
'''
#Returns s Series of ages
print(df['Age'])

#Returns a DataFrame of name and age
print(df[['Name', 'Age']])
'''

#Cleaning Data
df.dropna() #Remove rows with missing values
df.fillna(0) #Fill missing values with 0
df.drop_duplicates() #Remove duplicate rows
df.rename(columns={'Name': 'Full Name'}, inplace=True) #Rename 'Name' column to 'Full Name'
print(f"After cleaning: \n{df}")

#Filter and Sort Data
df[df['Age'] > 25] #Filter the rows by age
df.sort_values('Age') #Sort by Ages
df.sort_values(['Age', 'Full Name'], ascending=[True, False])

#Aggregation and Grouping
df['Age'].mean()
df.groupby('Full Name')['Age'].mean()

#Visualizing Data
df['Age'].plot(kind='hist') #Other plot types: 'bar', 'line', 'box', 'pie'
plt.show()
