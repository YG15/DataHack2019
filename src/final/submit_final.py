#!/usr/bin/env python3
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
import pandas as pd
import numpy as np

def run_IF(df,ms=100, rs=1):
    model = IsolationForest(behaviour = 'new', max_samples=ms, 
                          random_state = rs, contamination = 0)
    model.fit(df)
    anomaly_scores = model.decision_function(df)
    
    return anomaly_scores, model


selected_col = ['network_id',
                'device_id',
                'host_ipnunique',
                'outbound_bytes_countnanmax',
                'timestampcount',
                'timestampnunique',
                'timestamprange',
                'transport_protocolnunique',
                'port_dstnunique']

if __name__ == "__main__":
    featues_path = "./only_session_Features_no_log.csv"

    final_df = pd.read_csv(featues_path, index_col = 0)

    df_features = final_df[selected_col].fillna(final_df.mean())

    X = df_features.copy()
    X.drop(['device_id'], inplace=True, axis=1)

    # Run model
    anomaly_scores, model = run_IF(X,ms=1024, rs=42)
    anomaly_scores = -anomaly_scores

    results = pd.DataFrame({'network_id' : df_features.network_id, 'device_id' : df_features.device_id,'confidence' : anomaly_scores})
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
    
