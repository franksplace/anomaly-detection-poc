#!/usr/bin/env python3

import argparse
import pandas as pd
from pyod.models.iforest import IForest
from sklearn.preprocessing import LabelEncoder
import numpy as np

SYSLOG_COLS = ['month', 'day', 'time', 'hostname', 'service', 'pid', 'message']

def try_load_syslog_csv(file_path):
    df = pd.read_csv(file_path, low_memory=False)
    cols_lower = [c.lower() for c in df.columns]
    if set(SYSLOG_COLS).issubset(set(cols_lower)):
        col_map = {orig: SYSLOG_COLS[i] for i, orig in enumerate(cols_lower) if orig in SYSLOG_COLS}
        df.rename(columns=col_map, inplace=True)
        return df
    else:
        df_no_header = pd.read_csv(file_path, header=None, low_memory=False)
        if df_no_header.shape[1] == len(SYSLOG_COLS):
            df_no_header.columns = SYSLOG_COLS
            return df_no_header
    return None

def load_data(file_path):
    df = try_load_syslog_csv(file_path)
    if df is not None:
        return df, True
    df_generic = pd.read_csv(file_path, low_memory=False)
    return df_generic, False

def preprocess_syslog(df):
    for col in ['month', 'hostname', 'service']:
        le = LabelEncoder()
        df[col] = df[col].astype(str)
        df[col] = le.fit_transform(df[col])

    df['day'] = pd.to_numeric(df['day'], errors='coerce')
    df['pid'] = pd.to_numeric(df['pid'], errors='coerce')
    df['message_length'] = df['message'].astype(str).apply(len)
    df['digit_count'] = df['message'].astype(str).apply(lambda x: sum(c.isdigit() for c in x))

    def parse_time(t):
        try:
            h, m, s = t.split(':')
            return int(h), int(m), int(s)
        except Exception:
            return 0, 0, 0
    time_parsed = df['time'].apply(parse_time)
    df['hour'] = time_parsed.apply(lambda x: x[0])
    df['minute'] = time_parsed.apply(lambda x: x[1])
    df['second'] = time_parsed.apply(lambda x: x[2])

    feature_cols = ['month', 'day', 'hour', 'minute', 'second', 'hostname', 'service', 'pid', 'message_length', 'digit_count']
    features = df[feature_cols]
    features = features.replace([np.inf, -np.inf], np.nan)
    features = features.fillna(features.mean())
    features = features.dropna(axis=1, how='all')  # drop columns all-NaN
    features = features.dropna(axis=0)             # drop rows with any NaN
    return features

def preprocess_generic(df):
    df_num = df.apply(pd.to_numeric, errors='coerce')
    df_num = df_num.replace([np.inf, -np.inf], np.nan)
    df_num = df_num.fillna(df_num.mean())
    df_num = df_num.dropna(axis=1, how='all')
    df_num = df_num.dropna(axis=0)
    return df_num

def preprocess(df, is_syslog):
    if is_syslog:
        return preprocess_syslog(df)
    else:
        return preprocess_generic(df)

def detect_anomalies(data):
    model = IForest()
    model.fit(data)
    labels = model.labels_
    scores = model.decision_scores_
    return labels, scores

def main():
    parser = argparse.ArgumentParser(description='Anomaly Detection for syslog or generic CSV files with header detection')
    parser.add_argument('--input_file', type=str, required=True, help='CSV input file path')
    parser.add_argument('--output_file', type=str, default='output.csv', help='CSV output results file path')
    args = parser.parse_args()

    df, is_syslog = load_data(args.input_file)
    features = preprocess(df, is_syslog)

    if features.empty:
        print('No features extracted from input file. Exiting.')
        return

    labels, scores = detect_anomalies(features)
    df['anomaly_label'] = labels
    df['anomaly_score'] = scores
    df.to_csv(args.output_file, index=False)
    print(f'Results saved to {args.output_file}')

if __name__ == '__main__':
    main()

