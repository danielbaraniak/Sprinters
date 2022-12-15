import time

from configparser import ConfigParser

from .sprinters_driver import SprintersDriver
from .scraper_utils import get_random_number_from_range
from .scraper_utils import get_flat_ox_data, get_flat_otd_data, dump_csv_dict_data

config = ConfigParser()
config.read('settings.cfg')
settings = dict(config.items('scraper'))


def main():
    sprinters = SprintersDriver()
    sprinters.move_to_site(settings['site'])

    cookies_closed = sprinters.close_cookies(
        [
            settings['button_accept_cookies'],
            settings['button_settings_cookies'],
            settings['button_save_preferences_cookies']
        ]
    )

    if not cookies_closed:
        exit('Could not close cookies. Exiting...')

    ox_links = []
    otd_links = []

    # getting links from site
    for _ in range(int(settings['max_pagination'])):
        js_objects = sprinters._find_elements_by_xpath(
            settings['advertisement_css_selector']
        )

        new_ox_links, new_otd_links = sprinters.get_links_from_advertisements(
            js_objects,
            settings['advertisement_css_selector_featured'],
            settings['advertisement_css_selector_href']
        )

        ox_links.extend(new_ox_links)
        otd_links.extend(new_otd_links)

        next_site = sprinters.get_next_href(
            settings['pagination_css_selector_parent'],
            settings['pagination_css_selector_child']
        )

        time.sleep(get_random_number_from_range(3, 5))
        sprinters.move_to_site(next_site)

    # gather data from links
    flats_data: list[dict] = []
    for ox_link in ox_links:
        flats_data.append(get_flat_ox_data(ox_link))
        time.sleep(get_random_number_from_range(4, 5))

    for otd_link in otd_links:
        flats_data.append(get_flat_otd_data(otd_link))
        time.sleep(get_random_number_from_range(4, 5))

    dump_csv_dict_data(flats_data)
