#%% Import

import pandas as pd
import numpy as np
import sklearn as sk
import matplotlib.pyplot as plt
import json
from urllib import request
import random
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.decomposition import PCA
import seaborn as sns
from keras.models import Model, load_model
from keras.layers import Input, Dense
from keras.callbacks import ModelCheckpoint, TensorBoard
from keras import regularizers

#%%  Function definitions
def run_IF(df):
    model = IsolationForest(behaviour = 'new', max_samples=100, 
                          random_state = 1, contamination = 0)
    model.fit(df)
    anomaly_scores = model.decision_function(df)
    
    return anomaly_scores

def submit_df(results):
    arr_to_submit = results.to_json(orient='values')
    
    leaderboard_name = "armis"
    host = "leaderboard.datahack.org.il"
    
    # Name of the user
    submitter = "The Whale and the Petunias"
    
    predictions = json.loads(arr_to_submit)
    
    jsonStr = json.dumps({'submitter': submitter, 'predictions': predictions})
    data = jsonStr.encode('utf-8')
    req = request.Request(f"https://{host}/{leaderboard_name}/api/",
                          headers={'Content-Type': 'application/json'},
                          data=data)
    resp = request.urlopen(req)
    print(json.load(resp))
    

#%% Read features file 
df_features = pd.read_csv('Features_no_log.csv')
df_features.drop(['Unnamed: 0'], inplace=True, axis=1)

#%% Drop features
#df_features.drop(list(df_features.columns[9:27].values), inplace=True, axis=1)

#%% Select features
#X = df_features[['network_id','device_id',
#                 'type_ip_camera','type_pc','type_printer','type_printer','type_tablet','type_voip','type_watch',
#                 'hostnunique','port_dstnunique','packets_countnanmax','outbound_bytes_countnanmax','inbound_bytes_countnanmax',                 
#                 'packet_lossnanmax','retransmit_countnanmax','latencynanmax','session_countnanmax']]

X = df_features[['network_id', 'device_id', 'hostnunique', 'host_ipnunique', 'port_dstnunique',
                 'timestampnunique', 'timestampcount', 'timestamprange', 'transport_protocolnunique',
                 'packets_countnanmin', 'packets_countnanmax', 'packets_countnanmean',
                 'packets_countnanmedian']]


#%% Run IF on entire dataset
# Run model
anomaly_scores = run_IF(X)
anomaly_scores = -anomaly_scores

# Save results
results = pd.DataFrame({'network_id' : df_features.network_id, 'device_id' : df_features.device_id,'confidence' : anomaly_scores})

#%% Submit
submit_df(results)


#%%
thres = -0.39
anom_ratio = np.sum(anomaly_scores<thres) / len(anomaly_scores)
print('Anomaly ratio: %.5f.' %anom_ratio)

#%% Generate training data for autoencoder
#X_ae = df_features[['network_id','device_id',
#                 'hostnunique','host_ipnunique','port_dstnunique','packets_countnanmin','packets_countnanmax',
#                 'outbound_bytes_countnanmin','outbound_bytes_countnanmax','inbound_bytes_countnanmin','inbound_bytes_countnanmax',                 
#                 'packet_lossnanmax','retransmit_countnanmax','latencynanmax','session_countnanmax',
#                 'outbound_packets_countnanmin','outbound_packets_countnanmax','inbound_packets_countnanmin','inbound_packets_countnanmax',
#                 'outbound_bytes_maxnanmax','inbound_bytes_maxnanmax','outbound_packet_size_maxnanmax',
#                 'inbound_packet_size_maxnanmax']]

X_ae = df_features[['network_id', 'device_id', 'hostnunique', 'host_ipnunique', 'port_dstnunique',
                 'type_ip_camera','type_pc','type_printer','type_printer','type_tablet','type_voip','type_watch',
                 'timestampnunique', 'timestampcount', 'timestamprange', 'transport_protocolnunique',
                 'packets_countnanmin', 'packets_countnanmax', 'packets_countnanmean',
                 'packets_countnanmedian']]


#X_ae = X.copy()

for column in X_ae.columns:
    if column[0:4]!='type':
        X_ae[column] = StandardScaler().fit_transform(X_ae[column].values.reshape(-1, 1))

X_train = X_ae.iloc[anomaly_scores > thres]

X_train, X_test = train_test_split(X_train, test_size=0.5, random_state=1)

#%% Autoencoder

nb_epoch = 300
batch_size = 256
input_dim = X_train.shape[1] #num of columns, 179
encoding_dim = 16
hidden_dim = 12#int(encoding_dim / 2) #i.e. 25
learning_rate = 1e-7

input_layer = Input(shape=(input_dim, ))
encoder = Dense(encoding_dim, activation="tanh", activity_regularizer=regularizers.l1(learning_rate))(input_layer)
encoder = Dense(hidden_dim, activation="relu")(encoder)
decoder = Dense(hidden_dim, activation='tanh')(encoder)
decoder = Dense(input_dim, activation='relu')(decoder)
autoencoder = Model(inputs=input_layer, outputs=decoder)


#%%
autoencoder.compile(metrics=['accuracy'],
                    loss='mean_squared_error',
                    optimizer='adam')

cp = ModelCheckpoint(filepath="autoencoder_fraud.h5",
                               save_best_only=True,
                               verbose=0)

tb = TensorBoard(log_dir='./logs',
                histogram_freq=0,
                write_graph=True,
                write_images=True)

history = autoencoder.fit(X_train, X_train,
                    epochs=nb_epoch,
                    batch_size=batch_size,
                    shuffle=True,
                    validation_data=(X_test, X_test),
                    verbose=1,
                    callbacks=[cp, tb]).history
                          
#%% Load saved model
autoencoder = load_model('autoencoder_fraud.h5')

#%%
plt.plot(history['loss'], linewidth=2, label='Train')
plt.plot(history['val_loss'], linewidth=2, label='Test')
plt.legend(loc='upper right')
plt.title('Model loss')
#plt.ylabel('Loss')
#plt.xlabel('Epoch')
#plt.ylim(ymin=0.70,ymax=1)
#plt.show()


#%% Now run the trained model on our entire dataset
X_full_predictions = autoencoder.predict(X_ae)
mse = np.mean(np.power(X_ae - X_full_predictions, 2), axis=1)

autoencoder_results = pd.DataFrame({'network_id' : df_features.network_id, 'device_id' : df_features.device_id,'confidence' : np.sqrt(mse)})

#%%
submit_df(autoencoder_results)
#%%
fig = plt.figure()
plt.scatter(anomaly_scores, np.sqrt(mse),s=1)
fig.suptitle('IF vs autoencoder scores', fontsize=20)
#plt.xlabel='Isolated Forest Score'
#plt.ylabel='AutoEncoder Score'
#fig.xlabel('xlabel', fontsize=18)
#fig.ylabel('ylabel', fontsize=16)
#sns.kdeplot(anomaly_scores, np.sqrt(mse))

#%% Generate random submission dF
num_devices = df_devices.shape[0]
scores = np.arange(0,num_devices,1) / num_devices
random.shuffle(scores)

df_to_submit = pd.DataFrame()
df_to_submit['network_id'] = df_devices['network_id']
df_to_submit['device_id'] = df_devices['device_id']
df_to_submit['condidence'] = scores



