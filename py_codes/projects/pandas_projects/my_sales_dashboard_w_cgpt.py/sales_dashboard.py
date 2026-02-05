import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


#Reading data from dataset
file_path = Path(__file__).parent / "Superstore.csv"
df = pd.read_csv(file_path, encoding='ISO-8859-1')

#Verifying it's reading correctly
#print(f"First 5 entries to data set: \n{df.head()}\n")
#df.info()

#Cleaning the data

'''
#Clean up white spaces around column names
#df.columns = df.columns.str.strip()
#print(df.columns)

#Need to change the order and ship date from oject types to datetime types
#print(df.dtypes)
#df['Order Date'] = pd.to_datetime(df['Order Date'])
#df['Ship Date'] = pd.to_datetime(df['Ship Date'])
#print(df.dtypes)

#Check for missing values in dataset column by column
#print(df.isnull().sum())

#Drop the rows that contain missing values
#df.dropna(inplace=True)

#Check for duplicate rows
#print(df.duplicated().sum())

#Remove duplicated rows
#df.drop_duplicates(inplace=True)
'''

#Exploratory Analysis of data

'''
#Find total sales revenue
#print(df['Sales'].sum())

#Find the average sales value per order
#print(df['Sales'].mean())

#Find total sales by product category
#print(df.groupby(['Category'])['Sales'].sum())

#Find total profit for each subcategory
#print(df.groupby(['Sub-Category'])['Profit'].sum())

#Find how sales changed month to month(Time-based analysis)
#df['Order Date'] = pd.to_datetime(df['Order Date'])
#df['Order Month'] = df['Order Date'].dt.to_period('M')
#print(df.groupby(['Order Month'])['Sales'].sum())

#Find total sales per month
#print(df.groupby(['Order Month'])['Sales'].sum())

#Plot the results of the previous groupby
#df.groupby(['Order Month'])['Sales'].sum().plot(kind='line')
#plt.show()
'''

#Deeper Insights and KPI's(Key performance indicators)

'''
#Find the top 10 products by total sales
#print(df.groupby(['Product Name'])['Sales'].sum().sort_values(ascending=False).head(10))

#Find the top 10 least profitable products
#print(df.groupby(['Product Name'])['Profit'].sum().sort_values(ascending=True).head(10))

#Find the states that generate the most sales overall
#print(df.groupby(['State'])['Sales'].sum().sort_values(ascending=False).head(50))

#Find which sub-categories are high sales but low total profit
#print(df.groupby(['Sub-Category'])[['Sales', 'Profit']].sum())

#Find if there are bigger discounts on high-selling products
#print(df.groupby(['Product Name'])[['Sales', 'Discount']].mean())
'''

#Visualizations
'''
#Create  line chart to reveal trends of Order Month and sales
#df['Order Date'] = pd.to_datetime(df['Order Date'])
#df['Order Month'] = df['Order Date'].dt.to_period('M')
#df.groupby(['Order Month'])['Sales'].sum().plot(kind='line')
#plt.show()

#Create a bar chart for total sales and category
#df.groupby(['Category'])['Sales'].sum().plot(kind='bar')
#plt.show()

#Create horizontal bar chart to show profit by sub-category
#df.groupby(['Sub-Category'])['Profit'].sum().plot(kind='barh')
#plt.show()

#Compare total sales across regions using stacked bar chart
#df.groupby(['Region', 'Category'])['Sales'].sum().unstack().plot(kind='bar', stacked=True)
#plt.show()

#Find the distribution of sales values across different product categories using a blox plot
#df.boxplot(column='Sales', by='Category')
#plt.show()

#Create a heatmap that visualizes the correlation between numeric columns(like Sales, Profit, Discount, etc)
#numeric_df = df.select_dtypes(include='number')
#sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm')
#plt.show()
'''