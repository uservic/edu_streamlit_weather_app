import view
from apicall import OpenWeatherClient
import utils


def init_and_get_OW_client():
    city_coords = utils.get_city_coordinates()
    cl = OpenWeatherClient(city_coords)

    return cl


def process_main_page(api_client):
    view.show_main_page()
    view.process_side_bar_inputs(api_client)


if __name__ == '__main__':
    cl = init_and_get_OW_client()
    process_main_page(cl)
    # api_key = "58890305bc38c1e9168bdbbcd5fad653"
    # api_key = "wrongKey"
