import pandas as pd
import numpy as np


def get_network_hierarchy(network_df):
  """
  input: a table of network connection
  output: the same table with additional columns representing the level of hierarchy in the net
  IMPORTANT: the function assumes there each device has it unique id regardless the network it is in, if there are
  duplicates ids, the function will results incorrect results
            thus it is recommended to run the function on each network separately or to change the devices ids so
            they won't be any shared ids across networks
  """
  # Correct columns values from float tp integers
  network_df['full_service_device_id'] = [str(int(network))+'_'+str(int(device)) if ~np.isnan(device) else None\
                                          for network,device in zip(network_df.network_id,network_df.service_device_id)]
  network_df['full_device_id']         = [str(int(network))+'_'+str(int(device)) if ~np.isnan(device) else None\
                                          for network,device in zip(network_df.network_id,network_df.device_id)]
  
  output_devices = list(network_df.full_device_id.unique())
  input_devices  = list(network_df.full_service_device_id.unique())
  root_devices   = list(set(output_devices).difference(set(input_devices)))
  
  device_level = 0
  network_df['network_hierarchy'] = np.nan
  
  while len(root_devices)>0:
    network_df['network_hierarchy'] = [device_level+1 if device in root_devices else val for device, val in zip(network_df.full_device_id,network_df.network_hierarchy)]
    root_devices = list(network_df.full_service_device_id[network_df.network_hierarchy==device_level+1])
    device_level+=1
  return(network_df)