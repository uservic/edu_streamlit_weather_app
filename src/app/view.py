import numpy as np
import streamlit as st
from PIL import Image
import pandas as pd
import utils
import model
import plotly.express as px


def show_main_page():
    st.set_page_config(
        layout="wide",
        initial_sidebar_state="auto",
        page_title="Weather Analyzer Demo"
    )
    st.write(
        """
        # Анализ температурных данных и мониторинг текущей температуры через :orange[OpenWeatherMap API]
        """
    )


def set_sidebar_image(sidebar):
    image = Image.open(utils.get_resources_dir() + "weather_icon.jpg")
    st.sidebar.image(image)


def get_display_data(curr_weather) -> dict:
    d = dict()
    if curr_weather:
        d["curr_temp"] = curr_weather["main"]["temp"]
    else:
        d["error"] = "Данные недоступны"

    return d


def prepare(data):
    if "curr_temp" in data:
        t = round(data["curr_temp"])
        data["curr_temp"] = t

    return data


def get_input_data():
    raw_data = st.sidebar.file_uploader("Загрузить файл с данными", type={"csv", "txt"}, help="CSV, TXT")
    if raw_data is not None:
        try:
            df = pd.read_csv(raw_data, parse_dates=['timestamp'])
            return df[["city", "timestamp", "temperature", "season"]]
        except:
            st.error(":red[Ошибка парсинга файла. Будут спользоваться архивные данные!]")
    return model.open_local_data()


def process_side_bar_inputs(api_client):
    set_sidebar_image(st.sidebar)
    st.sidebar.header('Заданные пользователем параметры')
    user_input_df = sidebar_input_features()

    city = user_input_df["CityEng"].values[0]
    api_key = user_input_df["ApiKey"].values[0]
    from_date = user_input_df["FromDate"].values[0]

    df = get_input_data()

    tab1, tab2 = st.tabs(["Текущее", "Исторические данные"])
    with tab1:
        raw_data = api_client.get_current_weather(city, api_key)
        curr_weather = process_response(raw_data, st)

        data = get_display_data(curr_weather)
        prepared_data = prepare(data)

        write_curr_temp_data(prepared_data)
        process_current_temp(prepared_data, city, df)
    with tab2:
        city_rus = user_input_df["CityRus"].values[0]
        st.write(f"## :red[{city_rus}]")
        historic_analyze(city, df, from_date)


def sidebar_input_features():
    city = st.sidebar.selectbox("Город", utils.get_russian_city_names())

    api_key = st.sidebar.text_input("Ключ для api OpenWeather")
    from_date = st.sidebar.selectbox("Исторические данные начиная с", utils.get_year_start_dates())

    data = {
        "CityEng": utils.get_city_name_translation(city),
        "CityRus": city,
        "ApiKey": api_key,
        "FromDate": from_date
    }

    df = pd.DataFrame(data, index=[0])

    return df


def process_current_temp(prepared_data, city: str, df):
    stat_desc_table = model.get_desc_table(city, df)

    curr_season = utils.get_current_season()
    season_rus = utils.get_season_rus(curr_season)

    if stat_desc_table.empty or curr_season not in stat_desc_table.values:
        st.write("### :red[Не найдены данные для города!]")
        return

    mean = stat_desc_table.loc[stat_desc_table["season"] == curr_season, ("temperature", "mean")].values[0]
    std = stat_desc_table.loc[stat_desc_table["season"] == curr_season, ("temperature", "std")].values[0]

    if np.isnan(mean) or np.isnan(std):
        st.write(":red[Невозможно рассчитать средние для города!]")
        return

    left = round(mean - 2 * std)
    right = round(mean + 2 * std)

    with st.container():
        st.write(
            f" **:green[Нормальный]** диапазон температур по всем историческим данным для сезона {season_rus}: **{left}\N{DEGREE SIGN} -- {right}\N{DEGREE SIGN}**"
        )
        if not "error" in prepared_data:
            if left <= prepared_data["curr_temp"] <= right:
                st.write(f"Температура воздуха в **:green[нормальном]** диапазоне")
                st.image(utils.get_resources_dir() + "weather_ok_icon.jpg", width=200)
            else:
                st.write(f"Температура воздуха **:red[аномальна!]**")
                st.image(utils.get_resources_dir() + "weather_attent_icon.jpg", width=200)


def write_curr_temp_data(df):
    if "error" in df:
        err_msg = df["error"]
        st.write(f":red[{err_msg}]")
    else:
        color = "blue"
        sign = ""
        temp = str(df["curr_temp"])
        if df["curr_temp"] > 0:
            color = "orange"
            sign = "+"

        st.write(f"#### Текущая температура воздуха: :{color}[{sign}{temp}\N{DEGREE SIGN}]")


def historic_analyze(city: str, hist_df, from_date="2019-01-01"):
    df = hist_df
    df = df[df["timestamp"] >= from_date]
    if df.empty:
        st.write("### :red[Не найдены данные для города за указанный период!]")
        return

    avg_30d_df = model.get_city_30d_avg_df(city, df)
    if avg_30d_df.empty:
        st.write("### :red[Не найдены данные для города!]")
        return

    draw_historic_30d_avg_chart(avg_30d_df)

    stat_desc_table = model.get_desc_table(city, df)
    write_seasonal_mean_std_table(stat_desc_table)

    draw_anomalies_chart(avg_30d_df, stat_desc_table)


def draw_historic_30d_avg_chart(df):
    chart_data = df[["timestamp", "temperature", "mov_avg_30day"]]

    fig = px.line(chart_data, x="timestamp", y=["temperature", "mov_avg_30day"])
    fig['data'][1]['line']['color'] = 'rgb(255, 1, 1)'
    fig.update_layout(title="Значения температуры и 30-ти дневная скользящая средняя", xaxis_title="date",
                      yaxis_title="temperature", legend_title="")
    st.plotly_chart(fig, use_container_width=True)


def write_seasonal_mean_std_table(df):
    st.write("##### Средние значения и стандартное отклонение температуры по сезонам")
    res_df = df[["season", "temperature"]].reset_index(drop=True)
    st.write(res_df)


def draw_anomalies_chart(df, stat_desc_df):
    anom_data = model.get_anomalies_df(df, stat_desc_df)

    fig = px.line(df, x="timestamp", y=["mov_avg_30day"])
    fig.add_scatter(x=anom_data["timestamp"], y=anom_data["temperature"], mode='markers',
                    marker=dict(color="red", size=10), name="seasonal anomaly")
    fig.update_layout(title="30-ти дневная скользящая средняя температуры и сезонные аномалии", xaxis_title="date",
                      yaxis_title="temperature")
    st.plotly_chart(fig, use_container_width=True)


def process_response(raw_rs: dict, st) -> dict:
    if raw_rs["cod"] != 200:
        if raw_rs["cod"] == 401:
            st.error({"cod": 401,
                      "message": "Invalid API key. Please see https://openweathermap.org/faq#error401 for more info."})
        else:
            st.error("Something went wrong! HTTP{code}".format(code=raw_rs["cod"]))
        st.image(utils.get_resources_dir() + "husky_huh_icon.jpg", width=200)
        return dict()

    return {"weather": raw_rs["weather"],
            "main": raw_rs["main"],
            "name": raw_rs["name"]}
