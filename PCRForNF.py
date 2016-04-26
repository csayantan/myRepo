from nsepy import get_history
from datetime import date
import pandas as pd
import requests
from io import BytesIO 
import certifi
from scipy import stats
from dateutil.relativedelta import relativedelta
import numpy as np
#import matplotlib.pyplot as plt
import datetime
import numpy as np
import matplotlib.colors as colors
import matplotlib.finance as finance
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import talib as ta
from talib import MA_Type
import statsmodels as sm



nf_calls=[]
nf_puts=[]


#nf_calls[['VolumeCalls']]=np.nan
#nf_puts[['VolumeCalls']]=np.nan
i=min_avalable_strikes=4850
max_avalable_strike=9400
nf_opt_CE=nf_opt_PE=pd.DataFrame()

while i in range(min_avalable_strikes,max_avalable_strike):
    temp_CE = get_history(symbol="NIFTY",
                         start=date(2016,2,1), 
                         end=date(2016,4,24),
                         index=True,
                         option_type="CE",
                         strike_price=i,
                         expiry_date=date(2016,4,28))
    
    #print(nf_opt_CE.head())
    #if nf_opt_CE['Number of Contracts'].values >0 :
    '''if nf_opt_CE.empty :
        nf_opt_CE.append(0)
    '''
    
    temp_PE = get_history(symbol="NIFTY",
                         start=date(2016,2,1), 
                         end=date(2016,4,22),
                         index=True,
                         option_type="PE",
                         strike_price=i,
                         expiry_date=date(2016,4,28))
    #nf_opt_PE.rename(columns = {'Number of Contracts':'Volume'}, inplace = True)
    #nf_opt_CE.rename(columns = {'Number of Contracts':'Volume'}, inplace = True)

    #temp_CE=temp_CE.drop(temp_CE[temp_CE['Number of Contracts']>0.0].index)
    #temp_PE=temp_PE.drop(temp_CE[temp_CE['Number of Contracts']>0.0].index)
    nf_opt_CE=pd.concat([nf_opt_CE,temp_CE]).drop_duplicates()
    nf_opt_PE=pd.concat([nf_opt_PE,temp_PE]).drop_duplicates()
    nf_opt_CE.index=pd.to_datetime(nf_opt_CE.index)
    nf_opt_PE.index=pd.to_datetime(nf_opt_PE.index)
    i=i+50
    #print(i)

#print(nf_opt_PE.head())
nf_opt_PE.drop_duplicates(inplace=True)
nf_opt_CE.drop_duplicates(inplace=True)
#print(nf_opt_PE.head(100))

nf_opt_PE.rename(columns = {'Number of Contracts':'Volume'}, inplace = True)
nf_opt_CE.rename(columns = {'Number of Contracts':'Volume'}, inplace = True)

nf_opt_PE.drop(['Symbol','Expiry','Open','High' ,'Low','Last','Settle Price','Turnover','Open Interest'  ,'Change in OI','Underlying'],axis=1,inplace=True)

nf_opt_CE.drop(['Symbol','Expiry','Open','High' ,'Low','Last','Settle Price','Turnover','Open Interest','Change in OI','Underlying'],axis=1,inplace=True)

nf_opt_PE = nf_opt_PE[nf_opt_PE.Volume > 0]
nf_opt_CE = nf_opt_CE[nf_opt_CE.Volume > 0]
#print(nf_opt_PE.tail())

##priceCrossVolume###
nf_opt_PE['PESum']=nf_opt_PE.groupby(level=0)['Premium Turnover'].sum()
nf_opt_CE['CESum']=nf_opt_CE.groupby(level=0)['Premium Turnover'].sum()

#nf_puts= nf_opt_CE['Number of Contracts']*nf_opt_CE['Close']
#print(nf_calls.head())


nf_opt_PE.drop(['Volume','Close'],axis=1,inplace=True)
nf_opt_CE.drop(['Volume','Close'],axis=1,inplace=True)
#print(nf_opt_PE.index.Date)
#nf_opt_PE['Summation']=

wPCR= (nf_opt_PE['PESum']/nf_opt_CE['CESum'])
#wPCR.rename(columns = {'0':'wPCR'}, inplace = True)
#color=plt.rainbow(np.linspace(0,1,n))
#color=iter(plt.rainbow(np.linspace(0,1,n)))
#c=next(color)
wPCR.plot()
plt.show()

print(wPCR.head(500))
#print(nf_opt_PE.tail(500))

