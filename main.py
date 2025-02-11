#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import glob
import os.path 
import matplotlib.pyplot as plt
import datetime
import seaborn as sns
import folium
import requests
import urllib.parse
import datetime
from io import BytesIO
from PIL import Image
import calendar


# In[2]:


stationdf = pd.read_csv('datasets/station_information.csv')   

stationdf.head()


# In[3]:


"""
Cleaning:
The first column of `datasets/station_information.csv` corresponds to the label
so it's better to use the pd.read_csv(..., index_col=0) named argument to set the index 
to that column's values
"""

stationdf = pd.read_csv('datasets/station_information.csv', index_col=0)


stationdf.head()


# In[4]:


"""
Cleaning:
There's a few columns we're interested in,
we could use pd.read_csv(..., usecols=['lat', 'lon', ...etc...]) but
instead we'll use pd.DataFrame.drop(columns=[...]) to discard the columns
we don't need
"""

unneeded_cols = ['altitude', 'capacity', 'is_charging_station', 'rental_methods', 'obcn', 'short_name', '_ride_code_support', 'is_valet_station', 'cross_street', 'groups', 'nearby_distance']

cleaned_df = stationdf.drop(columns=unneeded_cols)
cleaned_df


# In[5]:


locations = cleaned_df[['station_id', 'lat', 'lon']]
locations


# In[6]:


google_static_maps_api = 'https://maps.googleapis.com/maps/api/staticmap'

markers = [(x, y) for x, y in zip(locations['lat'], locations['lon'])]
markers[:3]


# In[7]:


"""
Information:
------------------------------------------------
From https://developers.google.com/maps/documentation/maps-static/start#Markers
The markers parameter defines a set of one or more markers (map pins) at a set of locations. 
Each marker defined within a single markers declaration must exhibit the same visual style; if 
you wish to display markers with different styles, you will need to supply multiple markers parameters 
with separate style information.

The markers parameter takes set of value assignments (marker descriptors) of the following format:

markers=markerStyles|markerLocation1| markerLocation2|... etc.

The set of markerStyles is declared at the beginning of the markers declaration and consists of zero or 
more style descriptors separated by the pipe character (|), followed by a set of one or more locations 
also separated by the pipe character (|).
------------------------------------------------


latitude and longitude take 6 decimal places, hence the f'{:.6f}' format_spec in the following fstring

"""

center_lat = locations['lat'].mean()
center_lon = locations['lon'].mean()

params = {
#    'center': '43.651070,-79.347015',
    'center': '43.6742200301605, -79.39451997301134',
    'markers': 'color:blue|' + '|'.join([f'{lat:.6f},{lon:.6f}' for lat, lon in markers[:600]]),
    'format': 'jpg',
#    'scale': 1,
    'size': '400x400',
    'key': 'AIzaSyCj1qERpT2VI_hOsPonR25vG8b6A-yfMZ8'
}
len(markers)
center_lat, center_lon


# In[8]:


"""

center_lat = sum(lat for lat, lon in markers) / len(markers)
center_lon = sum(lon for lat, lon in markers) / len(markers)

(43.67422003016046, -79.3945199730113)
ChatGPT gave us this code and the answer is the same as yours, but takes longer to run. A+ Rob
""" 


# In[9]:


response = requests.get(google_static_maps_api, params=params)

if response.status_code == 200:
    with open('images/bike_stations.jpg', 'wb') as f:
        f.write(response.content)


# In[10]:


encoded_params = urllib.parse.urlencode(params)


# In[11]:


def generate_ridership_csv():
    ridership_csv = glob.glob("datasets/bikeshare-ridership-2023/*.csv")

    ridership_df = pd.concat([pd.read_csv(file, encoding = 'cp1252') for file in ridership_csv], ignore_index = True)

    ridership_df.to_csv("datasets/combined_ridership.csv", index = False)

    print(" Combined CSV files successfully!")

if os.path.isfile("datasets/combined_ridership.csv"):
    print("Combined_ridership.csv file already exists")
else:
    generate_ridership_csv()


# In[12]:


# Find the number of total rows to determine our sampling frequency
rows_df = pd.read_csv("datasets/combined_ridership.csv", encoding='cp1252')

row_count = len(rows_df)

print(f"Total number of rows in the CSV: {row_count}")


# In[13]:


"""We want a systematic sample of 10,000 rows of data

Therefore, n = 5,713,141 / 10,000

"""
sample_size = 10000
interval = row_count / sample_size

print(f"Interval: {interval}")


# In[14]:


# Use ILOC to pickup every 571 row and create new csv file


sample_df = rows_df.iloc[::571].copy()

if os.path.isfile("datasets/sample_every_571_row.csv"):
    print("sample_every_571_row.csv file already exists")
else:
    sample_df.to_csv("datasets/sample_every_571_row.csv", index=False)
    print("✅ Sampled every 571 row and saved to new file!")



# In[15]:


#Lets see what our data looks like in a PD Dataframe

sample_df.head()


# In[16]:


#Split data in Start time so the date and time have their own columns (for start and end date/time)

if ('Start Date' not in sample_df.columns and 'End Date' not in sample_df.columns and 'Time Start' not in sample_df.columns and 'Time End' not in sample_df.columns):
    sample_df.loc[:, 'Start Date'] = pd.to_datetime(sample_df.loc[:, 'Start Time']).dt.date
    sample_df.loc[:, 'Time Start'] = pd.to_datetime(sample_df.loc[:, 'Start Time']).dt.time
    sample_df.loc[:, 'End Date'] = pd.to_datetime(sample_df.loc[:, 'End Time']).dt.date
    sample_df.loc[:, 'Time End'] = pd.to_datetime(sample_df.loc[:, 'End Time']).dt.time


    #Drop old Start time and End Time columns and other irrelevant columns
    sample_df = sample_df.drop(columns=['Start Time', 'End Time', 'Trip Id'])
sample_df.head()


# In[17]:


#Find column data types
sample_df.dtypes


# In[18]:


#Rename columns for better functionality
sample_df.columns = ['Trip id'] + list(sample_df.columns[1:])

sample_df = sample_df.fillna({'Trip id': 0})


# In[19]:


#Remove any rows with nan values

sample_df = sample_df.dropna(subset=['Start Station Name', 'End Station Name'])
sample_df.isnull().sum()
sample_df.head()

#Test to see if Trip ID column had 0 filled in on the nan rows
sample_df.to_csv("datasets/test.csv", index = False)


# In[20]:


print(sample_df.columns)


# In[21]:


#Print final 
print(f"{len(sample_df)}")
sample_df.head()

sample_df = pd.merge(sample_df, locations, left_on='Start Station Id', right_on='station_id', how='left')
sample_df

sample_df = pd.merge(sample_df, locations, left_on='End Station Id', right_on='station_id', how='left', suffixes=('_start', '_end'))
sample_df = sample_df.dropna()

sample_df.to_csv("datasets/lon-lat.csv")


# In[22]:


# Rearrange columns and column names for easier presentation

new_order = ['Trip id', 'Start Date', 'Time Start', 'End Date', 'Time End', 'Trip  Duration', 'Start Station Id', 'Start Station Name',
             'End Station Id', 'End Station Name', 'User Type', 'Bike Id', 'lat_start', 'lon_start', 'lat_end', 'lon_end']

sample_df = sample_df[new_order]

sample_df.rename(columns={'Trip  Duration': 'Trip Duration (seconds)', 'Start Date': 'Start Date (YYYY-MM-DD)', 'End Date': 'End Date (YYYY-MM-DD)'}, inplace = True)


sample_df.head()


# In[23]:


#Check data types
sample_df.dtypes


# In[24]:


#Convert start date and end date from object to datetime

sample_df['Start Date (YYYY-MM-DD)'] = pd.to_datetime(sample_df['Start Date (YYYY-MM-DD)'], format = '%Y-%m-%d')
sample_df['End Date (YYYY-MM-DD)'] = pd.to_datetime(sample_df['End Date (YYYY-MM-DD)'], format = '%Y-%m-%d')
sample_df['Time Start'] = pd.to_datetime(sample_df['Time Start'], format = '%H:%M:%S')
sample_df['Time End'] = pd.to_datetime(sample_df['Time End'], format = '%H:%M:%S')

sample_df.dtypes


# In[25]:


#confirm that there are no more missing values
print(sample_df.isnull().sum().sum())


# In[26]:


#Confirm there are no duplicated rows
print(sample_df.duplicated().sum())


# In[27]:


#Confirm columns are correct data types

sample_df.dtypes


# In[28]:


# Data is now fully cleaned, lets move on to data analysis


# In[29]:


#Look at the breakdown of casual members vs annual members
user_type_counts_df = sample_df['User Type'].value_counts().reset_index()
user_type_counts_df.columns = ['User Type', 'Count']
print(user_type_counts_df)


# In[30]:


#Table showing riders by month, as well as the percentage of the overall rides

sample_df['Month'] = sample_df['Start Date (YYYY-MM-DD)'].dt.to_period('M')

#Group by Month and get count

start_date_by_month = sample_df.groupby('Month').size().reset_index(name='Count')
# Calculate the percentage for each month
start_date_by_month['Percentage'] = (start_date_by_month['Count'] / start_date_by_month['Count'].sum()) * 100

# Add a total row
total_row = pd.DataFrame({'Month': ['Total'], 'Count': [start_date_by_month['Count'].sum()], 'Percentage': [100]})
start_date_by_month = pd.concat([start_date_by_month, total_row], ignore_index=True)

print(start_date_by_month)


# In[31]:


# •	Identify fluctuations in bike usage throughout the year, comparing peak and off-peak seasons.

#Table showing riders by month, as well as the percentage of the overall rides

sample_df['Month'] = sample_df['Start Date (YYYY-MM-DD)'].dt.to_period('M').astype(str)

#Group by Month and get count

start_date_by_month_user = sample_df.groupby(['Month', 'User Type']).size().reset_index(name='Count')

# Calculate the percentage for each month
start_date_by_month_user['Percentage'] = (start_date_by_month_user['Count'] / start_date_by_month_user['Count'].sum()) * 100

# Add a total row
# Add a total row for each User Type
total_row = start_date_by_month_user.groupby('User Type').sum().reset_index()
total_row['Month'] = 'Total'
total_row['Percentage'] = 100

# Add a grand total row for all users
grand_total_row = pd.DataFrame({'Month': ['Total'], 'User Type': ['All'], 'Count': [start_date_by_month_user['Count'].sum()], 'Percentage': [100]})

# Combine everything
final_table = pd.concat([start_date_by_month_user, total_row, grand_total_row], ignore_index=True)

# Display the result
import IPython.display as display
display.display(final_table)


# In[32]:


bar_chart_users = final_table.drop(columns='Percentage')  # Drop the 'Percentage' column if it exists

# Filter out the 'Total' row
bar_chart_users = bar_chart_users[bar_chart_users['Month'] != 'Total']

# Pivot the table to have 'User Type' as columns
bar_chart_users_pivot = bar_chart_users.pivot_table(index='Month', columns='User Type', values='Count', aggfunc='sum', fill_value=0)

# Plot the bar chart with stacking enabled
bar_chart = bar_chart_users_pivot.plot(kind='bar', stacked=True, figsize=(10, 6), color=['blue', 'green'])

# Adding labels and title
plt.title('Count of User Types by Month')
plt.xlabel('Month')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.legend(title='User Type', loc='upper left', labels=['Annual Member', 'Casual Member'], fontsize=12, title_fontsize=14)


# Display the plot
plt.show()
    
fig = bar_chart.get_figure()
fig.savefig('images/fig1.png')


# In[33]:


#•	Analyze daily and hourly ridership patterns to determine high-demand periods, especially during commute hours.

#Look at the day of the week for our sample

day_of_week = sample_df["Start Date (YYYY-MM-DD)"].dt.day_name()
sample_df['Day of Week'] = sample_df['Start Date (YYYY-MM-DD)'].dt.day_name()
sample_df.head()


# In[34]:


day_counts = sample_df['Day of Week'].value_counts()

# Plot the pie chart
pie = day_counts.plot(kind='pie', figsize=(8, 8), autopct='%1.1f%%', startangle=90, cmap='rainbow')

# Adding title
plt.title('Distribution of Days of the Week')

# Display the plot
plt.show()
fig = pie.get_figure()
fig.savefig('images/fig2.png')


# In[35]:


"""

It is very interesting to see that the rider volume is consistent every day of the week. This suggests that the program is used by people for a variety of purposes. The decrease of weekday commuters is 
replaced by people who are getting around the city to go to different venues on weekends.

"""


# In[36]:


sample_df['day_start'] = sample_df['Time Start'].apply(lambda x: pd.Timedelta(f'{x.hour}:{x.minute}:{x.second}'))


sample_df['day_start_hour'] = sample_df['day_start'].dt.components.hours
sample_df['day_start_minute'] = sample_df['day_start'].dt.components.minutes
sample_df['day_start_seconds'] = sample_df['day_start'].dt.components.seconds
sample_df


# In[37]:


# showing most busy bike use hours.
f = sample_df['day_start_hour'].plot(kind='hist', bins=24, color='coral', edgecolor = 'black')

# Plot Histogram with Colors
plt.xlabel('Hour of Day (24-Hr)') #X-axis label
plt.ylabel('Frequency')
plt.xticks(range(0, 25, 1))
plt.title('Distribution of day start hour')

plt.show()

plt.savefig('images/fig3.png')


# In[38]:


"""
The modality of the data's distribution is bimodal, corresponding to the hours 8-9am and 5-6pm, which follows the expected rush hour patterns in the City of Toronto. 

See following code snippit below for modality figures.

"""


# In[39]:


url = 'https://raw.githubusercontent.com/leonkag/Statistics0/main/UniBiMultiModal.jpg'
page = requests.get(url)
img = Image.open(BytesIO(page.content))
img.resize((600, 300))




# In[40]:


sample_df.dtypes


# In[ ]:





# In[41]:


fig4 = sample_df.groupby('Month')['Month'].count()
fig4.plot(kind='bar' )

plt.xlabel('Month')
plt.ylabel('Usage')
plt.title('Total bike usage by month')
plt.savefig('images/fig4.png', bbox_inches='tight')

plt.show()


#print(sample_df.groupby('Month')['day_start_hour'].describe())  # Get min/max/mean


# In[42]:


sample_df['Month'] = pd.to_datetime(sample_df['Month'], format='%Y-%m')


# In[43]:


def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Fall'
sample_df['Season'] = sample_df['Month'].dt.month.map(get_season)

sample_df


# In[44]:


season_df = sample_df.groupby(['Season', 'Month']).size().reset_index(name='Count')


# In[45]:


season_df['Month_Number'] = season_df['Month'].dt.month


season_map = {
    0: "Winter", 1: "Winter", 11: "Winter",  # Dec, Jan, Feb
    2: "Spring", 3: "Spring", 4: "Spring",  # Mar, Apr, May
    5: "Summer", 6: "Summer", 7: "Summer",  # Jun, Jul, Aug
    8: "Fall", 9: "Fall", 10: "Fall"        # Sep, Oct, Nov
}

def month_num_to_name(x):
    if x in [12, 1, 2]:  # Dec, Jan, Feb -> Winter
        return 'Winter'
    elif x in [3, 4, 5]:  # Mar, Apr, May -> Spring
        return 'Spring'
    elif x in [6, 7, 8]:  # Jun, Jul, Aug -> Summer
        return 'Summer'
    elif x in [9, 10, 11]:  # Sep, Oct, Nov -> Fall
        return 'Fall'

# Apply function to get the Season column
# season_df['Season'] = season_df['Month_Number'].apply(month_num_to_name)
season_df.loc[season_df['Month_Number'] == 12, 'Month_Number'] = 0
season_df = season_df.sort_values(by='Month_Number')
season_df

season_df['Month_Name'] = ['Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov']
season_df


# In[46]:


"""
sns.lineplot(
    data=season_df, 
    x='Month_Name', 
    y='Count', 
    hue='Season', 
    marker='o', 
    palette='rainbow', 
    linewidth=2.5  # Increase the linewidth for darker lines
)
If the lines still don’t appear dark enough, you can:

Use a different palette: The rainbow palette has bright colors; you might try dark or deep instead:

python
Copy
Edit
palette='dark'
Manually define darker colors:

python
Copy
Edit
palette=['darkblue', 'darkred', 'darkgreen', 'black']
Increase contrast with edgecolor (if markers are hard to see):

python
Copy
Edit
sns.lineplot(..., markerfacecolor='black', markeredgewidth=2)


"""
f = plt.figure(figsize=(10, 6))
sns.lineplot(data=season_df, x = season_df['Month_Name'], y='Count', hue='Season', marker='o', palette='deep', linewidth=3)

# Labels and title
plt.xlabel("Month")
plt.ylabel("Count")
plt.title("Monthly Ride Frequency per Month (2023)")
plt.xticks(range(0, 12))  # Show full range of hours
plt.legend(title="Season")

# Show plot
plt.grid(True, linestyle='--', alpha=0.5)

plt.savefig('images/fig5.png')


# In[47]:


sample_df


# In[48]:


locations.to_csv('datasets/locations.csv')

sample_df


# In[49]:


sample_df['End Station Id'] = sample_df['End Station Id'].astype(np.int64)
sample_df



# In[50]:


new_locations = sample_df[['lat_start', 'lon_start', 'lat_end', 'lon_end']]
new_locations.isna().sum()


# In[51]:


import folium as folium

# Example list of tuples (latitude, longitude)
route = [
    (43.63985, -79.395989),
    (43.64012, -79.395672),
    (43.64045, -79.395321),
    (43.64100, -79.394956)
]

# Create a map centered around the first point
mymap = folium.Map(location=route[0], zoom_start=15)

# Add the route as a polyline
folium.PolyLine(route, color="blue", weight=2.5, opacity=1).add_to(mymap)

# Add markers for each point in the route
for lat, lon in route:
    folium.Marker([lat, lon]).add_to(mymap)

# Save the map as an HTML file
mymap.save("route_map.html")


# In[52]:


df = sample_df
df


# In[53]:


################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################


# In[ ]:




