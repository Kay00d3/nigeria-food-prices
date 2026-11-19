import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def time_ordered_split(
    df: pd.DataFrame,
    date_col: str = "year_month",
    train_ratio: float = 0.8,
):
    """Split chronologically by unique sorted periods so no future period leaks."""
    periods = sorted(df[date_col].unique())
    split_idx = int(len(periods) * train_ratio)
    train_periods = set(periods[:split_idx])
    test_periods = set(periods[split_idx:])

    train_df = df[df[date_col].isin(train_periods)].copy()
    test_df = df[df[date_col].isin(test_periods)].copy()
    return train_df, test_df


def compute_regression_metrics(y_true, y_pred, model_name: str = "Model") -> dict:
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    return {
        "model": model_name,
        "MAE": float(mean_absolute_error(y_true, y_pred)),
        "RMSE": rmse,
        "R2": float(r2_score(y_true, y_pred)),
        "n_test": int(len(y_true)),
    }


def naive_baseline_metrics(
    test_df: pd.DataFrame,
    current_price_col: str,
    target_col: str,
) -> dict:
    """Naive benchmark: next month's price equals this month's price."""
    return compute_regression_metrics(
        y_true=test_df[target_col],
        y_pred=test_df[current_price_col],
        model_name="Naive (t+1 = t)",
    )