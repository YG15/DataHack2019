#log
# features (log)
feature_cols=['packets_count',
       'outbound_bytes_count', 'inbound_bytes_count', 'packet_loss',
       'retransmit_count', 'latency', 'session_count',
       'outbound_packets_count', 'inbound_packets_count', 'outbound_bytes_max',
       'outbound_bytes_min', 'outbound_bytes_mean', 'outbound_bytes_median',
       'outbound_bytes_stddev', 'inbound_bytes_max', 'inbound_bytes_min',
       'inbound_bytes_mean', 'inbound_bytes_median', 'inbound_bytes_stddev',
       'outbound_packet_size_max', 'outbound_packet_size_min',
       'outbound_packet_size_mean', 'outbound_packet_size_median',
       'outbound_packet_size_stddev', 'inbound_packet_size_max',
       'inbound_packet_size_min', 'inbound_packet_size_mean',
       'inbound_packet_size_median', 'inbound_packet_size_stddev']

general_cols=['network_id','device_id','timestamp']
first=True
for col in feature_cols:
    cols=[general_cols[0],general_cols[1],general_cols[2],col]
    #unique id
    df1= session_df[cols]
    df1['uniq_id']=df1['network_id'].astype(str)+'.'+df1['device_id'].astype(str)    
    df1.set_index('uniq_id', inplace=True)
    # log
    df1[col]=np.log10(df1[col]+1)
    df1.head()
    # join devices
    df_feature= df1.join(devices_df['type'], on='uniq_id', how='left',lsuffix='_left', rsuffix='_right')
    df_feature.reset_index(inplace=True)
    # add column of average er type and timestamp
    df_avgtime = df_feature.groupby(['type','timestamp'],as_index=False).agg({col:'mean'})
    df_avgtime.head()
    df_feature2= df_feature.merge(df_avgtime, how='left', on=['type','timestamp'])
    #subtract average
    df_feature2['residual_'+col]= df_feature2[col+'_x']-df_feature2[col+'_y']
    df_feature2['uniq_id']=df_feature2['uniq_id'].astype('float')
    if first:
      feature_residuals= df_feature2[['network_id','device_id','residual_'+col]]
      first =False
    else:
      feature_residuals['residual_'+col]= df_feature2['residual_'+col]