'''
Problem 2
This problem concerns moving averages.
'''

'''
1. Download the monthly mean total sunspot number from 1/1749 until now from http://www.sidc.be/silso/datafiles 
and read it into a pandas dataframe. Plot the sunspot number from 1749 until now, and also for the last 77 years.
'''

from datetime import datetime


cols = ['Year','Month','Date_frac','Mean_Total','Mean_Std_Dev','Observations','Marker']
sun = pd.read_csv('http://www.sidc.be/silso/DATA/SN_m_tot_V2.0.csv',sep=';',header=None,names=cols)
sun['Day'] = 1
dates = [datetime(*x) for x in zip(sun['Year'], sun['Month'], sun['Day'])]
sun.index = dates
sun.drop(['Year','Month','Day'],axis=1, inplace=True)

fig, (ax0, ax1) = plt.subplots(nrows=2, figsize=(15, 7), sharey=True)

ax0.plot(sun['Date_frac'], sun['Mean_Total'])
ax0.title.set_text("Mean Total Sunspots from 1749 to Present")
ax0.set_xlabel('Year')
ax0.set_ylabel('Mean Total Sunspots')
plt.subplots_adjust(hspace = 0.5)
sun77yrsago = sun['Date_frac'] >= 2017-77+(9.0-1)/12
ax1.plot(sun[sun77yrsago]['Date_frac'],sun[sun77yrsago]['Mean_Total'],)
ax1.title.set_text("Mean Total Sunspots in the Last 77 Years")
ax1.set_xlabel('Year')
ax1.set_ylabel('Mean Total Sunspots')

'''
2. Calculate and plot the moving average of the data for the last 77 years with a 13 month window. 
Plot both the original data and the moving average of the data on the same graph. 
Use the rolling functionality of pandas to accomplish this. Provide two such plots. 
One with win_type set to the default value, and one with win_type=parzen.
'''

sun77 = sun[sun77yrsago].copy(deep=True)
sun77['Moving_Avg'] = sun77['Mean_Total'].rolling(13).mean()

sun77['Moving_Avg_p'] = sun77['Mean_Total'].rolling(13,win_type='parzen').mean()

fig, (ax0, ax1) = plt.subplots(nrows=2, figsize=(15, 7))

x = sun77.index.to_pydatetime()

ax0.plot(x, sun77['Mean_Total'], label='mean total')
ax0.plot(x, sun77['Moving_Avg'], label='13-mo moving average', linewidth=3, alpha=0.5,color='k')
ax0.legend(loc='upper center', bbox_to_anchor=(0.5, 1.0),ncol=3, fancybox=True, shadow=True, numpoints=1)
ax0.title.set_text("Total Sunspots in the Last 77 Years")
ax0.set_ylabel('Number of Sunspots')

plt.subplots_adjust(hspace = 0.5)

ax1.plot(x, sun77['Mean_Total'], label='original')
ax1.plot(x, sun77['Moving_Avg_p'], label='13-mo moving average in Parzen windows', linewidth=3, alpha=0.5,color='k')
ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.0),ncol=3, fancybox=True, shadow=True, numpoints=1)
ax1.title.set_text("Mean Total Sunspots in the Last 77 Years")
ax1.set_xlabel('Year')
ax1.set_ylabel('Mean Number of Sunspots')

'''
3. Provide a third plot that shows the difference in the two moving averages calculated in the previous step.
'''

fig, ax2 = plt.subplots(nrows=1, figsize=(15, 3.5))

ax2.plot(x, sun77['Moving_Avg_p']-sun77['Moving_Avg'], label='difference in moving averages')
ax2.legend(loc='upper center', bbox_to_anchor=(0.5, .22),ncol=3, fancybox=True, shadow=True, numpoints=1)
ax2.title.set_text("Mean Total Sunspots in the Last 77 Years")
ax2.set_xlabel('Year')
ax2.set_ylabel('Mean Number of Sunspots')
