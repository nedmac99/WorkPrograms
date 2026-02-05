import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

files = ["worldometer_data.csv", "time_series_covid19_confirmed_global.csv", "time_series_covid19_deaths_global.csv"]

file_path = Path(__file__).parent / files[0]
file_path2 = Path(__file__).parent / files[1]
file_path3 = Path(__file__).parent / files[2]
df = pd.read_csv(file_path, encoding='ISO-8859-1')
df2 = pd.read_csv(file_path2, encoding='ISO-8859-1')
df3 = pd.read_csv(file_path3, encoding='ISO-8859-1')

#Cleaning up the data

df.columns = df.columns.str.strip()
df2.columns = df2.columns.str.strip()
df3.columns = df3.columns.str.strip()
#print(df.head())
#df.info()

#Analysis of the data

#Counting the null values per column
#print(df.isnull().sum())
#df.dropna(inplace=True)

#Find the top 10 Countries with the highest TotalCases
#print(df.sort_values('TotalCases', ascending=False).head(10))

#Find the countries that have the highest death rate
df['DeathRate'] = df['TotalDeaths'] / df['TotalCases']
#print(df.sort_values('DeathRate', ascending=False).head())

#Find countries with high total cases but low deaths using deathrate
#print(df[(df['TotalCases'] > 100000) & (df['DeathRate'] < 0.01)])

#Find the countries with the highest death rate despite low case counts
#print(df[(df['TotalCases'] < 50000) & (df['DeathRate'] > .05)])

#Find confirmed cases per million people
df['CasesPerMillion'] = (df['TotalCases'] * 1000000) / (df['Population'])
#print(df.sort_values('CasesPerMillion', ascending=False).head())

#Find out how many deaths per million
df['DeathsPerMillion'] = (df['TotalDeaths'] * 1000000) / (df['Population']) 
#print(df.sort_values('DeathsPerMillion', ascending=False).head())

#Find percent of cases recovered
df['RecoveryRate'] = (df['TotalRecovered']) / (df['TotalCases'])
#print(df.sort_values('RecoveryRate', ascending=False).head(10))

#Visualizations

#Chart top 10 countries by cases per million in descending order
#df.sort_values('CasesPerMillion', ascending=False).head(10).plot(kind='bar', x='Country/Region', y='CasesPerMillion')
#plt.show()

#Chart top 10 countries by deaths per million
#df.sort_values('DeathsPerMillion', ascending=False).head(10).plot(kind='bar', x='Country/Region', y='DeathsPerMillion')
#plt.show()

#Chart top 10 recovery rates with horizontal bar graph
#df.sort_values('RecoveryRate', ascending=False).head(10).plot(kind='barh', x='Country/Region', y='RecoveryRate')
#plt.show()

#Chart top 10 death rates with a vertical bar chart
#df.sort_values('DeathRate', ascending=False).head(10).plot(kind='bar', x='Country/Region', y='DeathRate')
#plt.show()

#Time-Series Analysis for confirmed cases
#df2.info()
#print(df2.head())

#Reshape data so that first 4 columns('Province/State', 'Country/Region', 'Lat', 'Long') stay fixed and all the remaining date columns become rows with one column for Date and one column for Confirmed cases
df2_melted = pd.melt(df2, id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], var_name='Date', value_name='Confirmed')

#Convert 'Date' to a datetime type for future filtering and analysis
df2_melted['Date'] = pd.to_datetime(df2_melted['Date'], format='%m/%d/%y')

#Find how the virus spread over time globally. Group by date and sum the confimed cases. Prints the first 20 dates
#print(df2_melted.groupby(['Date'])['Confirmed'].sum().head(20))

#Visualize the trend with a line graph
#df2_melted.groupby(['Date'])['Confirmed'].sum().head(10000).plot(kind='line')
#plt.show()

#Filter to only include rows from Italy
#df2_melted[df2_melted['Country/Region'] == 'Italy'].groupby(['Date'])['Confirmed'].sum().head(100).plot(kind='line')
#plt.show()

#Filter df2_melted to include only rows where Country/Region are in the list of 'Italy', 'USA', 'Brazil', 'India', 'China'
#print(df2_melted[df2_melted['Country/Region'].isin(['Italy', 'USA', 'Brazil', 'India', 'China'])].head(15))

#Group and plot the previous statement
#df2_melted[df2_melted['Country/Region'].isin(['Italy', 'USA', 'Brazil', 'India', 'China'])].groupby(['Date', 'Country/Region'])['Confirmed'].sum().unstack().plot(kind='line', stacked=True)
#plt.show()

#Convert from cumulative totals to daily new totals by calculating the difference between each row and the previous row and plot it using line graph
#df2_melted[df2_melted['Country/Region'].isin(['Italy', 'USA', 'Brazil', 'India', 'China'])].groupby(['Date', 'Country/Region'])['Confirmed'].sum().unstack().diff().plot(kind='line')
#plt.show()

#Smoothen the line of the graph in the last line using rolling to collect the average over a 7 day window
#df2_melted[df2_melted['Country/Region'].isin(['Italy', 'USA', 'Brazil', 'India', 'China'])].groupby(['Date', 'Country/Region'])['Confirmed'].sum().unstack().diff().rolling(window=7).mean().plot(kind='line')
#plt.show()

#Analyze Per Capita Daily Cases by normalizing daily new cases by population, so we can fairly compare countries of different sizes
daily_cases = df2_melted[df2_melted['Country/Region'].isin(['Italy', 'USA', 'Brazil', 'India', 'China'])].groupby(['Date', 'Country/Region'])['Confirmed'].sum().unstack().diff()
population = df.set_index('Country/Region')['Population']
daily_per_million = (daily_cases / population) * 1000000

#Plot the previous line using a smooth line with rolling()
daily_per_million.rolling(window=7).mean().plot(kind='line')
plt.show()

#Reshape data from df3 using melt to have a long format vs wide format. Add Column for date with values equivalent to deaths
df3_melted = pd.melt(df3, id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], var_name='Date', value_name='Deaths')
print(df3_melted)

#Convert date to datetime type
df3_melted['Date'] = pd.to_datetime(df3_melted['Date'], format='%m/%d/%y')

#Continue using the Learn Pandas chat in chatgpt