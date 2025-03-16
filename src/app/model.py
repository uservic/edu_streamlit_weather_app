import pandas as pd
import streamlit as st

import utils


def open_local_data(path=utils.get_resources_dir() + "temperature_data.csv"):
    df = pd.read_csv(path, parse_dates=['timestamp'])
    df = df[["city", "timestamp", "temperature", "season"]]

    return df


def get_city_30d_avg_df(city: str, df, window_len=30):
    df_sorted_ts = df.loc[(df["city"] == city), ["season", "city", "timestamp", "temperature"]].sort_values(by=["timestamp"])
    df_sorted_ts["mov_avg_30day"] = df_sorted_ts["temperature"].rolling(window=window_len).mean()

    return df_sorted_ts


def get_desc_table(city:str, df):
    df_city_seas_temp = df[["season", "city", "temperature"]]
    desc = df_city_seas_temp.groupby(["season", "city"]).describe()
    res = desc[[("temperature", "mean"), ("temperature", "std")]].reset_index()
    res = res[res["city"] == city]

    return res


def get_anomalies_df(df, stat_desc_df):
    seasons_stat = stat_desc_df[["season", "temperature"]].reset_index(drop=True)

    d = seasons_stat.to_dict("index")
    stats_dict = get_stats_dict(d)

    df["mean"] = df.season.map(lambda x: stats_dict[x][0])
    df["std"] = df.season.map(lambda x: stats_dict[x][1])

    res = df[(df["temperature"] > (df["mean"] + 2*df["std"])) | (df["temperature"] < (df["mean"] - 2*df["std"]))]

    return res


def get_stats_dict(source) -> dict:
    res = dict()
    for i in range(len(source)):
        row_map = source[i]
        vals = []
        for v in row_map.values():
            vals.append(v)
        res[vals[0]] = (vals[1], vals[2])

    return res
