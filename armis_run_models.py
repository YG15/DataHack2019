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

#%%  Run IF function
def run_IF(df):
    model = IsolationForest(behaviour = 'new', max_samples=100, 
                          random_state = 1, contamination = 0)
    model.fit(df)
    anomaly_scores = model.decision_function(df)
    
    return anomaly_scores

#%% Read features file (v1)
df_features = pd.read_csv('features_v1.csv')

#%% Read features file (v2)
df_features = pd.read_csv('features_v2.csv')
df_features['type'][26566] = 'PC' # TEMPORARY!!! 
df_features.drop(['model','manufacturer','operating_system','operating_system_version'], inplace=True, axis=1)
df_features.fillna(0, inplace=True)

#%% Read features file (v3)
df_features = pd.read_csv('features_v3 (3).csv')
#na_devices = df_features['real_device_'].isna()

# Drop devices that don't appear in any network
#df_features.drop(df_features[na_devices].index, axis=0, inplace = True)

#df_features['device_id']  = [ str(val).split('.')[0] for val in df_features.real_device_]
# Drop columns I can't use
df_features.drop(['Unnamed: 0'], inplace=True, axis=1)

# Replace NaNs with 0
#df_features.fillna(0, inplace=True)

# Some more tweaking
#df_features.host_nunique = np.log10(df_features.host_nunique+1)
#df_features.host_ip_nunique = np.log10(df_features.host_ip_nunique+1)
#df_features.port_dst_nunique = np.log10(df_features.port_dst_nunique+1)
#df_features.timestamp_count = np.log10(df_features.timestamp_count+1)
#df_features.timestamp_range = np.log10(df_features.timestamp_range+1)

#%% Drop features
df_features.drop(list(df_features.columns[9:27].values), inplace=True, axis=1)

#%% Select features
X = df_features[['network_id','device_id',]]

#%% Run IF on entire dataset

# One-hot-encode type variable: 
#ohe = OneHotEncoder(handle_unknown='ignore')
#ohe_df = pd.DataFrame(ohe.fit_transform(df_features.type.values.reshape(-1,1)).toarray())
#ohe_df.columns = ohe.categories_[0]
#df_features = pd.concat([df_features, ohe_df], axis=1)
#df_features.drop(['type'], axis=1, inplace=True)

# Create training data
#X = df_features.copy()
#X.drop(['device_id'], inplace=True, axis=1)

# Run model
anomaly_scores = run_IF(X)
anomaly_scores = -anomaly_scores

# Save results
results = pd.DataFrame({'network_id' : df_features.network_id, 'device_id' : df_features.device_id,'confidence' : anomaly_scores})

#%% Run IF separately on device types

results = pd.DataFrame()
device_types = np.unique(df_features.type)
for device_type in device_types:
    # Create training data
    df_type = df_features[df_features.type == device_type]
    X = df_type.copy()
    X.drop(['device_id','type'], inplace=True, axis=1)
    # Run model
    anomaly_scores = run_IF(X)
    anomaly_scores = -anomaly_scores
    # Concatenate results
    dev_type_results = pd.DataFrame({'network_id' : df_type.network_id, 'device_id' : df_type.device_id,'confidence' : anomaly_scores})
    if results.shape[0]==0:
        results = dev_type_results
    else:
        results = pd.concat([results,dev_type_results], axis=0)
            
#%% Run IF separately on networks
# One-hot-encode type variable: 
ohe = OneHotEncoder(handle_unknown='ignore')
ohe_df = pd.DataFrame(ohe.fit_transform(df_features.type.values.reshape(-1,1)).toarray())
ohe_df.columns = ohe.categories_[0]
df_features = pd.concat([df_features, ohe_df], axis=1)
df_features.drop(['type'], axis=1, inplace=True)

results = pd.DataFrame()
networks = np.unique(df_features.network_id)
for network in networks:
    # Create training data
    df_network = df_features[df_features.network_id == network]
    X = df_network.copy()
    X.drop(['device_id', 'network_id'], inplace=True, axis=1)
    # Run model
    anomaly_scores = run_IF(X)
    anomaly_scores = -anomaly_scores
    # Concatenate results
    network_results = pd.DataFrame({'network_id' : df_network.network_id, 'device_id' : df_network.device_id,'confidence' : anomaly_scores})
    if results.shape[0]==0:
        results = network_results
    else:
        results = pd.concat([results,network_results], axis=0)
        


#%% Submission

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







#%% Generate training data for autoencoder
thres = -0.36 # Set threshold high enough so that most anomalies should be detected (with many false alarms)

X_train = X.iloc[anomaly_scores > thres]

X_train.host_ip_nunique = np.log10(X_train.host_ip_nunique)
X_train.host_nunique = np.log10(X_train.host_nunique)
X_train.port_dst_nunique = np.log10(X_train.port_dst_nunique)
X_train.packets_count_min = np.log10(X_train.packets_count_min)

for column in X_train.columns:
    X_train[column] = StandardScaler().fit_transform(X_train[column].values.reshape(-1, 1))

X_train, X_test = train_test_split(X_train, test_size=0.05, random_state=1)

#%% Autoencoder
    
nb_epoch = 100
batch_size = 128
input_dim = X_train.shape[1] #num of columns, 30
encoding_dim = 8
hidden_dim = int(encoding_dim / 2) #i.e. 7
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
plt.ylabel('Loss')
plt.xlabel('Epoch')
#plt.ylim(ymin=0.70,ymax=1)
plt.show()


#%% Now run the trained model on our entire dataset
X_full_predictions = autoencoder.predict(X_train)
mse = np.mean(np.power(X - X_full_predictions, 2), axis=1)



#%% Generate random submission dF
num_devices = df_devices.shape[0]
scores = np.arange(0,num_devices,1) / num_devices
random.shuffle(scores)

df_to_submit = pd.DataFrame()
df_to_submit['network_id'] = df_devices['network_id']
df_to_submit['device_id'] = df_devices['device_id']
df_to_submit['condidence'] = scores



