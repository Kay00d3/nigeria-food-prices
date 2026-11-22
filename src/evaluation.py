import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

TARGET_COL = "price_ngn"
SHOCK_COLS = ["fx_lag1", "pms_lag1"]


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


def get_features(df: pd.DataFrame, include_shock: bool) -> list[str]:
    """Return base model features, optionally including shock columns."""
    base_features = (
        ["price_lag1", "price_lag2", "month_of_year"]
        + [c for c in df.columns if c.startswith(("mkt_", "com_"))]
    )
    return base_features + (SHOCK_COLS if include_shock else [])


def naive_benchmark(
    df: pd.DataFrame,
    date_col: str = "month",
    train_ratio: float = 0.8,
    current_price_col: str = "price_lag1",
    target_col: str = TARGET_COL,
) -> dict:
    """Compute naive baseline metrics on the time-ordered test set."""
    feats = get_features(df, include_shock=True)
    df_model = df.dropna(subset=feats + [target_col]).copy()
    _, test_df = time_ordered_split(df_model, date_col=date_col, train_ratio=train_ratio)
    metrics = naive_baseline_metrics(
        test_df, current_price_col=current_price_col, target_col=target_col
    )
    metrics["features"] = "baseline"
    return metrics


def run_experiment(
    df: pd.DataFrame,
    model,
    features: list[str],
    model_name: str,
    date_col: str = "month",
    train_ratio: float = 0.8,
    target_col: str = TARGET_COL,
) -> dict:
    """Fit a regression model on train_df and evaluate on test_df."""
    all_possible = get_features(df, include_shock=True)
    df_model = df.dropna(subset=all_possible + [target_col]).copy()
    train_df, test_df = time_ordered_split(
        df_model, date_col=date_col, train_ratio=train_ratio
    )

    model.fit(train_df[features], train_df[target_col])
    preds = model.predict(test_df[features])

    has_shocks = any(col in features for col in SHOCK_COLS)
    shock_label = "with shocks" if has_shocks else "no shocks"

    metrics = compute_regression_metrics(
        test_df[target_col], preds, model_name=f"{model_name} ({shock_label})"
    )
    metrics["features"] = shock_label
    return metrics