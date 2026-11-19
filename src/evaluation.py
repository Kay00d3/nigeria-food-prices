import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
 
TARGET = 'price_ngn'
TEST_START = '2025-10-01'   # roughly the last 8 months of the model data (Feb 2023 to May 2026); adjust after you see master.csv
SHOCK_FEATURES = ['fx_lag1', 'pms_lag1']

def get_features(df, with_shock):
    base = ['price_lag1', 'price_lag2', 'month_of_year']
    base += [c for c in df.columns if c.startswith('mkt_') or c.startswith('com_')]
    return base + SHOCK_FEATURES if with_shock else base

def split(df, test_start=TEST_START):
    cols = get_features(df, True) + [TARGET]
    df = df.dropna(subset=cols)
    return df[df['month'] < test_start], df[df['month'] >= test_start]

def score(y_true, y_pred):
    return {
        'MAE': mean_absolute_error(y_true, y_pred),
        'RMSE': float(np.sqrt(mean_squared_error(y_true, y_pred))),
        'R2': r2_score(y_true, y_pred),
    }

def run_experiment(df, model, features, name):
    train, test = split(df)
    model.fit(train[features], train[TARGET])
    res = score(test[TARGET], model.predict(test[features]))
    res['model'] = name
    res['features'] = 'with shock (Model A)' if 'fx_lag1' in features else 'without shock (Model B)'
    return res

def naive_benchmark(df):
    _, test = split(df)
    res = score(test[TARGET], test['price_lag1'])   # 'next month = this month'
    res.update({'model': 'Naive benchmark', 'features': 'last month price only'})
    return res
