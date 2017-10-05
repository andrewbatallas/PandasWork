'''
Problem 1
This problem concerns swimming records. 
'''

import pandas as pd

def process_time(x):
    x = x.replace(' (r)','')
    x = x.replace(' (e)','')
    if ":" in x:
        time = x.split(":")
        return 60.0*float(time[0]) + float(time[1])
    else:
        return float(x)

def process_file(file,column_names):
    d = pd.read_csv(file,header=None,names=column_names)
    d['Time']=d['Time'].apply(process_time)
    d['Date']=pd.to_datetime(d['Date'])
    return d

def process_frame(d):
    d['Time']=d['Time'].apply(process_time)
    d['Date']=pd.to_datetime(d['Date'])
    return d

'''    
1. Create a wr data frame that has a ’Gender’ column, and put all the men’s and women’s records, 
differentiated by event and gender, in one data frame.
'''

mf = pd.read_csv("100m-WR-free-M.csv",header=None,names=["Time","Type","Name","Nationality","Date","Place","Meet","Location","Ref"])
mf = process_frame(mf)

wf = process_file('100m-WR-free-W.csv',["Time","Type","Name","Nationality","Date","Place","Meet","Location","Ref"])

mb = pd.read_csv('100m-WR-back-M.tsv',names=['Time','Swimmer','Date','Place'],sep='\t')
mb = process_frame(mb)

wb = pd.read_csv('100m-WR-back-W.tsv',names=['Time','Swimmer','Date','Meet','Place'],sep='\t')
wb = process_frame(wb)

mbr = pd.read_csv('100m-WR-breast-M.tsv',names=['Time','Swimmer','Nationality','Date','Place'],sep='\t')
mbr = process_frame(mbr)

wbr = pd.read_csv('100m-WR-breast-W.tsv',names=['Time','Swimmer','Nationality','Date','Place'],sep='\t')
wbr = process_frame(wbr)

mfl = pd.read_csv('100m-WR-fly-M.tsv',names=['Time','Swimmer','Date','Place'],sep='\t')
mfl = process_frame(mfl)

wfl = pd.read_csv('100m-WR-fly-W.tsv',names=['Time','Swimmer','Date','Place'],sep='\t')
wfl = process_frame(wfl)

mf['Event']=pd.Series('freestyle',index=mf.index)
mf['Gender']=pd.Series('male',index=mf.index)
mb['Event']=pd.Series('backstroke',index=mb.index)
mb['Gender']=pd.Series('male',index=mb.index)
mbr['Event']=pd.Series('breaststroke',index=mbr.index)
mbr['Gender']=pd.Series('male',index=mbr.index)
mfl['Event']=pd.Series('butterfly',index=mfl.index)
mfl['Gender']=pd.Series('male',index=mfl.index)
wf['Event']=pd.Series('freestyle',index=wf.index)
wf['Gender']=pd.Series('female',index=wf.index)
wb['Event']=pd.Series('backstroke',index=wb.index)
wb['Gender']=pd.Series('female',index=wb.index)
wbr['Event']=pd.Series('breaststroke',index=wbr.index)
wbr['Gender']=pd.Series('female',index=wbr.index)
wfl['Event']=pd.Series('butterfly',index=wfl.index)
wfl['Gender']=pd.Series('female',index=wfl.index)

wr = pd.concat((mf[['Time','Date','Gender','Event']],mb[['Time','Date','Gender','Event']],
                mbr[['Time','Date','Gender','Event']],mfl[['Time','Date','Gender','Event']],
               wf[['Time','Date','Gender','Event']],wb[['Time','Date','Gender','Event']],
                wbr[['Time','Date','Gender','Event']],wfl[['Time','Date','Gender','Event']]),axis=0, ignore_index=True)

'''
2. Add the 200m individual medley (IM) data to the the data frame, for both men and women. This data can be found on Wikipedia.
'''

mim = pd.read_html("https://en.wikipedia.org/wiki/World_record_progression_200_metres_individual_medley",header=0)[0]
mim.rename(columns = {'TIME':'Time'}, inplace=True)
mim.rename(columns = {'DATE':'Date'}, inplace=True)
mim = process_frame(mim)
mim['Event']=pd.Series('medley',index=mim.index)
mim['Gender']=pd.Series('male',index=mim.index)

wim = pd.read_html("https://en.wikipedia.org/wiki/World_record_progression_200_metres_individual_medley",header=0)[2]
wim.rename(columns = {'TIME':'Time'}, inplace=True)
wim.rename(columns = {'DATE':'Date'}, inplace=True)
wim = process_frame(wim)
wim['Event']=pd.Series('medley',index=wim.index)
wim['Gender']=pd.Series('female',index=wim.index)

wr = pd.concat((wr[['Time','Date','Event','Gender']],mim[['Time','Date','Event','Gender']],
                wim[['Time','Date','Event','Gender']]),axis=0,ignore_index=True)

'''
#3. Add a column to the data frame that indicates the margin by which the new world record broke the old world record, 
for each entry. For the first entry in each event-gender category, enter NaN. Plot the margins by event in two plots, 
one for men and one for women. Make sure that there’s a legend that indicates which line corresponds to event, 
and that there’s a title indicating which margins are for men and which are for women.
'''

import numpy as np

%matplotlib inline
import matplotlib.pyplot as plt

wr['Margin'] = 0.0
for name, grp in wr.groupby(['Event','Gender']):
    start = grp.head(1).index.item()
    stop = grp.tail(1).index.item()
    wr.iloc[start, wr.columns.get_loc('Margin')] = np.nan
    for i in range(start+1,stop+1):
        wr.iloc[i, wr.columns.get_loc('Margin')] = wr['Time'][i-1] - wr['Time'][i]
        
fig,axes=plt.subplots(nrows=1,ncols=2,figsize=(20,10))

wr_no_dup = wr.drop_duplicates(subset=['Time','Event','Gender']) #since we want only record-breaking margins

for name, grp in wr_no_dup[wr_no_dup['Gender']=='male'].groupby('Event'):
    grp.plot(x='Date',y='Margin',ax=axes[0],label=name)
axes[0].title.set_text("Men's Record-Beating Margins by Event")
axes[0].set_xlabel('Year')
axes[0].set_ylabel('Margin (seconds)')

for name, grp in wr_no_dup[wr_no_dup['Gender']=='female'].groupby('Event'):
    grp.plot(x='Date',y='Margin',ax=axes[1],label=name)
axes[1].title.set_text("Women's Record-Beating Margins by Event")
axes[1].set_xlabel('Year')
axes[1].set_ylabel('Margin (seconds)')

'''
4. For each event, plot the male-to-female ratio of world records. This will be a little tricky, 
as the records for the men’s free, for example, were not set at the same time, nor do they have the same cardinality, 
as the women’s free. Do this in an intelligent way. One way might be to do it by year — a potential difficulty 
is that a world record might not have been set in a given year—figure out how to deal with that. 
Another way might be to plot a data point of the existing men’s wr divided by the existing women’s wr whenever 
a new record occurred in either category— but how you figure that out might be slightly challenging.
'''

ratio = pd.DataFrame(columns=['Event','Year','Ratio'])
ind = 0
for name, grp in wr.groupby('Event'):
    start_year = max(grp[grp['Gender']=='male']['Date'].min().year,grp[grp['Gender']=='female']['Date'].min().year)
    end_year = max(grp[grp['Gender']=='male']['Date'].max().year,grp[grp['Gender']=='female']['Date'].max().year)
    for i in range(start_year,end_year+1):
        m_record = grp[(grp['Gender']=='male') & (grp['Date'].dt.year <= i)]['Time'].min()
        w_record = grp[(grp['Gender']=='female') & (grp['Date'].dt.year <= i)]['Time'].min()
        ratio.loc[ind] = [name, i, m_record/w_record]
        ind += 1
        
fig,axes=plt.subplots(nrows=1,ncols=5,figsize=(20,5),sharey=True)
i = 0
for name, grp in ratio.groupby('Event'):
    grp.plot(x='Year',y='Ratio',ax=axes[i],label=name)
    axes[i].title.set_text("M-to-F Ratio of Swimming Records")
    i+=1

axes[0].set_ylabel('Ratio')
