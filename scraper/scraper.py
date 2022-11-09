from configparser import ConfigParser
from sprinters_driver import SprintersDriver
import time
def main():
    configparser = ConfigParser()
    configparser.read('config.ini')

    #load cached sites if not cached sites then search for them

    #sprinters = SprintersDriver(configparser.get('default', 'l'), configparser.get('default', 'p'))
    sprinters = SprintersDriver()

    sprinters.driver.get(configparser.get('default', 'site'))
    time.sleep(60)

    #cache sites and save data

if __name__ == '__main__':
    main()