# Summary of Findings 

## Objectives: 
The original intent of this project was to analyze Toronto Bikeshare program 2023 dataset to derive insights as to when, where, and how long riders were utilizing this service so as to better inform city planners for future bicycling lanes investments.

We used a variety of modules in Jupyter notebook such as Python, Pandas, Matplotlib, NumPy, Seaborn, Folium, as well as pulling data from various sources like Google maps. We arrived at the following conclusions about Toronto’s bikeshare program in 2023:

### Peak Usage Times:

Based on the data plotted on [fig3](/images/fig3.png) and further supported by [fig7](/images/fig7.png) (as well as [fig2's](/images/fig2.png) pie chart illustration), there are *clear peaks in bike usage during weekday mornings (7-9am), followed by evenings (5-7pm), which is attributable to common commuting hours.* This is an obvious *indication that the bikeshare system is heavily used by commuters, underscoring a need for more dedicated bike lanes during peak traffic times to enhance safety and efficiency standards of Torontonians.*

### Casual vs Annual Members:

It’s clear from [fig1](/images/fig1.png) bar chart that the overwhelming 90%+ of bikeshare program trips are conducted by casual members who do not have a bikeshare membership. Even more intriguing, besides annual members being such a small statistical group, they tend use the service more in the winter & spring months than in summer & fall months. This could indicate that the *bikeshare program may not be affordable enough to reach a higher conversion rate as well as market penetration in the public transportation space.* Therefore, city planners/administrators may investigate into pricing strategies to entice annual membership enrollment.

### High-Demand Stations:
Based on the bar chart shown in [fig8](/images/fig8.png) that highlights the bike capacity vs. trips taken compared to each bike station, it’s evident that majority of the high-volume stations have insufficient bike capacity. This imbalance is signaling the need for *increasing bike capacity at high-demand stations* and perhaps it would be wise to *re-direct some of the over-capacity bikes from other stations to the more underserved stations.*

### Trip travel durations:

From [fig6](/images/fig6.png) shows that an *overwhelming density of trips taken are in the range of 7-10 minutes, forming a right skew in the distribution of trips taken.* It would only make sense that *these short trips are taken in the downtown core where people would require subways, buses, or bikes to commute to work for short trip durations.* This is further supported by the [interactive heatmap](https://constcorrectness.github.io/toronto-bikeshare-2024/heatmap.html) showing *the high density of trips taken are in the downtown core.* Notable areas that demonstrated high volume of bike trips and should warrant attention: Distillery District, Union Station, Financial District core (eg. St Andrew station, King St & University, Welling St W & University), from College Station all the way to Toronto Eaton Centre, and lastly Yonge & Bloor area.

## Recommendations:

1. Add new bike lanes in already high-demand areas, especially near top-performing stations that would only get busier as Toronto’s population grows.

2. Seek expansion of bike lane coverage during weekday’s peak commuting hours in the morning and evening as subway stations are always overcrowded.

3. Increase bike capacity at busy stations and re-distribute bikes from underutilized ones.

4. Launch promotional campaigns to attract more casual users, thereby increasing overall usage.

5. Seek partnerships with private enterprises or large community groups to further promote and draw attention to the Bikeshare program.
The municipal government should monitor and develop policies that are not only bike commuting-friendly but also incentivize its citizenry to seek biking as an affordable, convenient, and safe method of transportation which would only generate long-term benefits to the city. Therefore these insights and recommendations aim to support the city’s proposal for expansion of bike lanes and procuring more bikes, ensuring a better bikeshare system. 
	