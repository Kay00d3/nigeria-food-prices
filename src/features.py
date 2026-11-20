import pandas as pd

def add_features(df):
    # df columns: month, zone, state, market, commodity, price_ngn, usd_ngn, pms_price
    out = []
    for (m, c), g in df.groupby(['market', 'commodity']):
        z, s = g['zone'].iloc[0], g['state'].iloc[0]
        g = g.sort_values('month').set_index('month').asfreq('MS')   # inserts missing months so shifts are correct
        g['market'], g['commodity'], g['zone'], g['state'] = m, c, z, s
        g['price_lag1'] = g['price_ngn'].shift(1)    # last month's price
        g['price_lag2'] = g['price_ngn'].shift(2)    # price two months ago
        g['fx_lag1'] = g['usd_ngn'].shift(1)         # last month's exchange rate
        g['pms_lag1'] = g['pms_price'].shift(1)      # last month's PMS price
        out.append(g.reset_index())
    res = pd.concat(out, ignore_index=True)
    res['month_of_year'] = res['month'].dt.month
    dummies = pd.get_dummies(res[['market', 'commodity']], prefix=['mkt', 'com'], dtype=int)
    return pd.concat([res, dummies], axis=1)