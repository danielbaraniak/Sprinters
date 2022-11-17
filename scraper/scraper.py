from configparser import ConfigParser
from sprinters_driver import SprintersDriver
import time

def main():
    configparser = ConfigParser()
    configparser.read('config.ini')

    #load cached sites if not cached sites then search for them
    site = configparser.get('default', 'site')

    #sprinters = SprintersDriver(configparser.get('default', 'l'), configparser.get('default', 'p'))
    sprinters = SprintersDriver()

    sprinters._move_to_site(site)

    cookies_closed = sprinters.close_cookies(
        [
            configparser.get('default', 'BUTTON_ACCEPT_COOKIES'), \
            configparser.get('default', 'BUTTON_SETTINGS_COOKIES'), \
            configparser.get('default', 'BUTTON_SAVE_PREFERENCES_COOKIES')
        ]
    )

    if not cookies_closed:
        exit('Could not close cookies. Exiting...')

    sprinters.move_to_next_site(configparser.get('default', 'PAGINATION_CSS_SELECTOR_PARENT'), configparser.get('default', 'PAGINATION_CSS_SELECTOR_CHILD'))
    
    time.sleep(6000)
    #cache sites and save data

if __name__ == '__main__':
    main()