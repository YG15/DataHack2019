#!/usr/bin/env python3
import pandas as pd
import numpy as np

def diff_list(li1, li2): 
    return (list(set(li1) - set(li2))) 

def get_categ_col_dummy (df):    
    numerical_columns = df.describe().columns
    categorical_cols=diff_list(df.columns,numerical_columns)
    
    categorial = df[categorical_cols]
    #to prevent case-sensitive separation to different categories:
    categorial=categorial.apply(lambda x: x.str.lower(), axis=1)
    categorial_dummies = pd.get_dummies(categorial)
    df.drop(columns=categorical_cols, inplace=True)
    df=df.join(categorial_dummies)
    return df

def range_list(val_list):
    min_val = min(val_list)
    max_val = max(val_list)

    return (max_val-min_val)

if __name__ == "__main__":
    device_path = "all_devices.csv"
    devices_df = pd.read_csv(device_path, index_col = 0)
    print(devices_df.head())

    keep_os = ['Android', 'iOS', 'Mac OS X', 'Windows', 'watchOS',
        'Watch OS', 'Tizen', 'Symbian', 'Miui OS', 'Linux',
        'Axis Firmware', 'Firefox OS', 'Cisco IOS-XE', 'Cisco IOS',
        'Debian', 'Link-OS', 'Cisco NX-OS']
    devices_df['operating_system'] = [ val if val in keep_os else 'OTHER' for val in devices_df.operating_system]
    devices_df.drop(columns =['operating_system_version','model','manufacturer'], inplace=True)
    devices_df = get_categ_col_dummy(devices_df)
    devices_df.head()


    sessions_path = "all_sessions.csv"
    sessions_df = pd.read_csv(sessions_path, index_col = 0)
    print(sessions_df.head())

    
    classic_functions = [np.nanmin,np.nanmax,np.nanmean,np.nanstd, np.nanmedian]

    df_gb = sessions_df.groupby(['network_id','device_id'],as_index=False).agg({'host':'nunique',
                                                        'host_ip':'nunique',
                                                        'port_dst':'nunique',
                                                        'timestamp':['nunique','count',('range', lambda x: range_list(x))],
                                                        'transport_protocol':'nunique',
                                                        'packets_count':classic_functions,
                                                        'outbound_bytes_count':classic_functions, 
                                                        'inbound_bytes_count':classic_functions, 
                                                        'packet_loss':classic_functions,
                                                        'retransmit_count':classic_functions, 
                                                        'latency':classic_functions, 
                                                        'session_count':classic_functions,
                                                        'outbound_packets_count':classic_functions, 
                                                        'inbound_packets_count':classic_functions, 
                                                        'outbound_bytes_max':classic_functions,
                                                        'outbound_bytes_min':classic_functions, 
                                                        'outbound_bytes_mean':classic_functions, 
                                                        'outbound_bytes_median':classic_functions,
                                                        'outbound_bytes_stddev':classic_functions, 
                                                        'inbound_bytes_max':classic_functions, 
                                                        'inbound_bytes_min':classic_functions,
                                                        'inbound_bytes_mean':classic_functions, 
                                                        'inbound_bytes_median':classic_functions, 
                                                        'inbound_bytes_stddev':classic_functions,
                                                        'outbound_packet_size_max':classic_functions, 
                                                        'outbound_packet_size_min':classic_functions,
                                                        'outbound_packet_size_mean':classic_functions, 
                                                        'outbound_packet_size_median':classic_functions,
                                                        'outbound_packet_size_stddev':classic_functions, 
                                                        'inbound_packet_size_max':classic_functions,
                                                        'inbound_packet_size_min':classic_functions, 
                                                        'inbound_packet_size_mean':classic_functions,
                                                        'inbound_packet_size_median':classic_functions, 
                                                        'inbound_packet_size_stddev':classic_functions})

    df_gb.columns = ["".join(x) for x in df_gb.columns.ravel()]


    final_df = pd.merge(devices_df, df_gb, how = 'right', on=['network_id','device_id'])
    print(devices_df.shape, df_gb.shape, final_df.shape)
    final_df = final_df.replace([np.inf, -np.inf], np.nan)
    final_df = final_df.fillna(0)

    final_df.to_csv('only_session_Features_no_log.csv')
