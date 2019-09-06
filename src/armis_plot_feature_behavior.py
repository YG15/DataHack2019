#%% Import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns

#%% define read_csv_skipping_rows function
def read_csv_skipping_rows(csv_path, skip_ratio):
    def file_len(fname):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1
    
    len_of_file = file_len(csv_path)
    print ('file length %d, reading 1 in %d...' %(len_of_file, skip_ratio))    
    skipped = np.setdiff1d(np.arange(len_of_file), np.arange(0,len_of_file,10))
    
    df = pd.read_csv(csv_path, skiprows=skipped)
    print('Done.')
    return df
    
#%% Initialize
sessions_path = 'Armis Data/all_sessions.csv'
devices_path = 'Armis Data/all_devices.csv'

df_devices = pd.read_csv(devices_path)
df_sessions = read_csv_skipping_rows(sessions_path, 5)

#%% Extract day and hour and merge 
# Load devices.csv
df_sessions['datetime'] = df_sessions.timestamp.apply(datetime.fromtimestamp)
df_sessions['day'] = df_sessions.datetime.apply(lambda x: x.day)
df_sessions['hour'] = df_sessions.datetime.apply(lambda x: x.hour)
#df_sessions['hour_cum'] = pd.DataFrame([(df_sessions.day-np.min(df_sessions.day))*24 + df_sessions.hour])
#df_sessions.drop(['datetime','timestamp'], inplace = True)
# Show list of column names in all_sessions.csv

df = pd.merge(df_sessions, df_devices, how='left',on=['network_id','device_id'])

column_names = pd.read_csv(sessions_path, nrows=1).columns
print(column_names)
device_types = np.unique(df.type)
print(device_types)

#%% Look at single feature distribution
selected_feature = 'packets_count'
plt.subplot(2,1,1)
sns.kdeplot(df[selected_feature])
plt.subplot(2,1,2)
sns.kdeplot(np.log10(df[selected_feature]+1))

#%% Look at single feature over time
selected_feature = 'inbound_packet_size_mean'
separate_networks = False
separate_days = False
take_log = False
# load column and merge pre-loaded data

if take_log==True:
    df['log_'+selected_feature] = np.log10(df[selected_feature])
    selected_feature = 'log_'+selected_feature

for i, device_type in enumerate(device_types):

    df_type = df[df.type == device_type]

    y = df_type[selected_feature]
    
    if separate_networks:
        plt.figure()
        for network in [0,1,2,3]:
            plt.subplot(2,2,network+1)
            plt.title(device_type)
            df_net = df_type[df_type.network_id==network]
            
            df_gb = df_net.groupby('hour')
            y_mean = df_gb[selected_feature].agg('mean')
#            y_std = df_gb[selected_feature].agg('std')
            plt.plot(y_mean)
#            plt.errorbar(range(0,24), y_mean, yerr=y_std, color='w')
#            y = df_net[selected_feature]
#            for day in [5,6,7,8,9,10]:
#                df_day = df_net[df_type.day==day]
#                y = df_day[selected_feature]
#                
#                df_gb = df_day.groupby('hour')
#                y_mean = df_gb[selected_feature].agg('mean')
#                y_std = df_gb[selected_feature].agg('std')
#            
#                #plt.plot(y_mean)
#                plt.errorbar(range(0,24), y_mean, yerr=y_std, color='w')
    else:
            
        #sns.jointplot(df_type.hour, y, kind='hex')
        g = sns.JointGrid(df_type.hour, y)
        g.plot_marginals(sns.distplot, color=".5")
        g.plot_joint(plt.hexbin, gridsize=24)
        plt.title(device_type)
        
        if separate_days:
            for day in [5,6,7,8,9,10]:
                df_day = df_type[df_type.day==day]
                y = df_day[selected_feature]
                
                df_gb = df_day.groupby('hour')
                y_mean = df_gb[selected_feature].agg('mean')
                y_std = df_gb[selected_feature].agg('std')
                y_stderr = y_std / np.sqrt(df_gb[selected_feature].agg('count'))
            
                plt.plot(y_mean)
        else:
            df_gb = df_type.groupby('hour')
            y_mean = df_gb[selected_feature].agg('mean')
            y_std = df_gb[selected_feature].agg('std')
            y_stderr = y_std / np.sqrt(df_gb[selected_feature].agg('count'))
            plt.errorbar(range(0,24), y_mean, yerr=y_std, color='w')
    
#%%

