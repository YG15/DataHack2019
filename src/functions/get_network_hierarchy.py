import pandas as pd
import numpy as np


def get_network_hierarchy(network_df)
  
  input a table of network connection
  output the same table with additional columns representing the level of hierarchy in the net
  IPORTANT the function assumes there each device has it unique id regardless the network it is in, if there are duplicates ids, the function will results incorrect results
            thus it is recommended to run the function on each network seperatly or to change the devices ids so they won't be any shared ids across networks
  
  network_df['service_device_id'] = network_df.service_device_id.apply(lambda x int(x))
  output_devices = list(network_df.device_id.unique())
  input_devices = list(network_df.service_device_id.unique())
  root_devices = list(set(output_devices).difference(set(input_devices)))
  device_level = 0
  network_df['network_hierarchy'] = np.nan
  while len(root_devices)0
    network_df['network_hierarchy'] = [device_level+1 if device in root_devices else val for device, val in zip(network_df.device_id,network_df.network_hierarchy)]
    root_devices = list(network_df.service_device_id[network_df.network_hierarchy==device_level+1])
    device_level+=1
  return(network_df)