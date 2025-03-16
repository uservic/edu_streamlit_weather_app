# Учебное приложение Анализ температурных данных и мониторинг текущей температуры через OpenWeatherMap API

Попробовать приложение [тута](https://eduappweatherapp-b5bxpfeqbzqworknxta9md.streamlit.app/)

## Некторые файлы

- `main.py`:  точка входа приложения
- `gen.py`: генерация тестовых исторических данных в формате csv
- `requirements.txt`: зафиксированные версии зависимостей проекта

## Локальный запуск

### Shell

Из корневой папки проекта выполнить:

```shell
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ streamlit run src/app/main.py
```
