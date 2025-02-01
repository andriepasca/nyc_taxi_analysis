from scipy import stats
import numpy as np

def cleaner (df,threshold):
    z = np.abs(stats.zscore(df))
    df_clean = df[(z < threshold).all(axis=1)]
    return df_clean

def csvconverter(df, url_destination):
  df.to_csv(url_destination, encoding='utf-8', index=False)

  

