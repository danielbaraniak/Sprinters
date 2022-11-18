from configparser import ConfigParser
from sprinters_driver import SprintersDriver
from scraper_utils import get_random_number_from_range
import time
from scraper_utils import get_flat_ox_data, get_flat_otd_data, dump_csv_dict_data

def main():
    configparser = ConfigParser()
    configparser.read('config.ini')

    site = configparser.get('default', 'site')

    sprinters = SprintersDriver()

    sprinters.move_to_site(site)

    cookies_closed = sprinters.close_cookies(
        [
            configparser.get('default', 'BUTTON_ACCEPT_COOKIES'), \
            configparser.get('default', 'BUTTON_SETTINGS_COOKIES'), \
            configparser.get('default', 'BUTTON_SAVE_PREFERENCES_COOKIES')
        ]
    )

    if not cookies_closed:
        exit('Could not close cookies. Exiting...')

    ox_links = []
    otd_links = []
    
    #getting links from site
    for _ in range(int(configparser.get('default', 'MAX_PAGINATION'))):
        js_objects = sprinters._find_elements_by_xpath(
            configparser.get('default', 'ADVERTISEMENT_CSS_SELECTOR')
        )
        print('got js objects')
        new_ox_links, new_otd_links = sprinters.get_links_from_advertisements(
            js_objects, 
            configparser.get('default', 'ADVERTISEMENT_CSS_SELECTOR_FEATURED'), 
            configparser.get('default', 'ADVERTISEMENT_CSS_SELECTOR_HREF')
        )
        ox_links.extend(new_ox_links)
        otd_links.extend(new_otd_links)

        next_site = sprinters.get_next_href(
            configparser.get('default', 'PAGINATION_CSS_SELECTOR_PARENT'), 
            configparser.get('default', 'PAGINATION_CSS_SELECTOR_CHILD')
        )
        time.sleep(get_random_number_from_range(2, 14))
        sprinters.move_to_site(next_site)
        
    #gather data from links
    flats_data: list[dict] = []
    for ox_link in ox_links:
        flats_data.append(get_flat_ox_data(ox_link))
        time.sleep(get_random_number_from_range(15, 60))
    
    for otd_link in otd_links:
        flats_data.append(get_flat_otd_data(otd_link))
        time.sleep(get_random_number_from_range(15, 60))
    
    dump_csv_dict_data(flats_data)

if __name__ == '__main__':
    main()