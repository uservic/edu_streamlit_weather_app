from datetime import datetime


def get_city_coordinates() -> dict:
    d = dict()
    d["Beijing"] = (39.904202, 116.407394)
    d["Berlin"] = (52.514985, 13.379551)
    d["Cairo"] = (30.050755, 31.246909)
    d["Dubai"] = (25.229762, 55.289311)
    d["London"] = (51.50735, -0.12776)
    d["Los Angeles"] = (34.05223, -118.24368)
    d["Mexico City"] = (19.43261, -99.13321)
    d["Moscow"] = (55.751244, 37.618423)
    d["Mumbai"] = (19.07598, 72.87766)
    d["New York"] = (40.71278, -74.00594)
    d["Paris"] = (48.85661, 2.35222)
    d["Rio de Janeiro"] = (-22.908333, -43.196388)
    d["Singapore"] = (1.290270, 103.851959)
    d["Sydney"] = (-33.86882, 151.20930)
    d["Tokyo"] = (35.68949, 139.69171)

    return d


def get_city_name_translation(city_name: str) -> dict:
    translation = {
        "Пекин": "Beijing",
        "Берлин": "Berlin",
        "Каир": "Cairo",
        "Дубай": "Dubai",
        "Лондон": "London",
        "Лос-Анджелес": "Los Angeles",
        "Мехико": "Mexico City",
        "Москва": "Moscow",
        "Мумбаи": "Mumbai",
        "Нью-Йорк": "New York",
        "Париж": "Paris",
        "Рио-де-Жанейро": "Rio de Janeiro",
        "Сингапур": "Singapore",
        "Сидней": "Sydney",
        "Токио": "Tokyo"
    }

    return translation[city_name]


def get_russian_city_names() -> tuple:
    return ('Пекин', 'Берлин', 'Каир', 'Дубай', 'Лондон', 'Лос-Анджелес', 'Мехико',
            'Москва', 'Мумбаи', 'Нью-Йорк', 'Париж', 'Рио-де-Жанейро', 'Сингапур',
            'Сидней', 'Токио')


def get_year_start_dates() -> tuple:
    return ("2019-01-01", "2018-01-01", "2017-01-01", "2016-01-01", "2015-01-01", "2014-01-01", "2013-01-01",
            "2012-01-01", "2011-01-01", "2010-01-01")


def get_current_season():
    curr_month = datetime.today().strftime('%B')

    return get_season(curr_month)


def get_season(month_name: str) -> dict:
    seasons = {
        "december": "winter",
        "january": "winter",
        "february": "winter",
        "march": "spring",
        "april": "spring",
        "may": "spring",
        "june": "summer",
        "july": "summer",
        "august": "summer",
        "september": "autumn",
        "october": "autumn",
        "november": "autumn"
    }

    return seasons[month_name.lower()]


def get_season_rus(season_name: str) -> dict:
    seasons = {
        "winter": "Зима",
        "spring": "Весна",
        "summer": "Лето",
        "autumn": "Осень"
    }

    return seasons[season_name.lower()]


def get_resources_dir():
    return "src/app/resources/"
