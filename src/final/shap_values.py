#!/usr/bin/env python3
import matplotlib.pyplot as plt
import json
import pandas as pd
import numpy as np
import shap

from submit_final import  run_IF, selected_col


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
    
    
    # Show SHAP values
    sample = 4534
    explainer = shap.KernelExplainer(model.decision_function,X[0:100])
    kernel_shap_values = explainer.shap_values(X.iloc[[sample]])
    print(kernel_shap_values)
    score = model.decision_function(X.iloc[[sample]])
    print(score)
    shap.force_plot(explainer.expected_value, kernel_shap_values, X.columns)
    print("Done")
