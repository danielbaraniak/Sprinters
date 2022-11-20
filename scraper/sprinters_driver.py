from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.service import Service as BraveService
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from time import sleep as time_sleep
from typing import List

from .scraper_utils import get_random_number_from_range

class SprintersDriver:
    def __init__(self) -> None:
        browser = get_random_number_from_range(1, 3)
        try:
            if browser == 1:
                self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
            elif browser == 2:
                self.driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
            elif browser == 3:
                self.driver = webdriver.Chrome(service=BraveService(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()))
        except Exception as err:
            print(err)

    def _find_element_by_class_name(self, element: str) -> WebElement:
        return self.driver.find_element(By.CLASS_NAME, element)
    
    def _find_element_by_id(self, element: str) -> WebElement:
        return self.driver.find_element(By.ID, element)
    
    def _find_element_by_css_selector(self, element: str) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR, element)
    
    def _find_element_by_xpath(self, xpath: str) -> WebElement:
        return self.driver.find_element(By.XPATH, xpath)
    
    def _find_child_element_by_xpath(self, element, xpath: str) -> WebElement:
        return element.find_element(By.XPATH, xpath)

    def _find_elements_by_xpath(self, xpath: str) -> List[WebElement]:
        return self.driver.find_elements(By.XPATH, xpath)

    def close_cookies(self, cookies_config_routes: List[str]) -> bool:
        which_route = get_random_number_from_range(1, 2)
        time_sleep(2)
        try:
            if which_route == 1:
                self._find_element_by_id(cookies_config_routes[0]).click()
                return True
            elif which_route == 2:
                time_sleep(1)
                self._find_element_by_id(cookies_config_routes[1]).click()
                self._find_element_by_class_name(cookies_config_routes[2]).click()
                return True
        except NoSuchElementException as ex:
            print(f'NoSuchElementException: {ex}')
            return True
        except ElementClickInterceptedException as ex:
            print(f'ElementClickInterceptedException: {ex}')
            return False
        return False
    
    def move_to_site(self, site: str) -> None:
        self.driver.get(site)
    
    def get_next_href(self, pagination_selector: str, pagination_xpath_child: str) -> str:
        return self._find_child_element_by_xpath(self._find_element_by_xpath(pagination_selector), pagination_xpath_child).get_attribute('href')
    
    def get_links_from_advertisements(self, js_objects, card_xpath_featured: str, card_xpath_href: str):
        ox_links = []
        otd_links = []
        for js_object in js_objects:
            try:
                self._find_child_element_by_xpath(js_object, card_xpath_featured)
                continue
            except NoSuchElementException:
                link_to_child_site = self._find_child_element_by_xpath(js_object, card_xpath_href).get_attribute('href')
                if link_to_child_site.startswith('https://www.otod'):
                    otd_links.append(link_to_child_site)
                    continue
                ox_links.append(link_to_child_site)
        return ox_links, otd_links
            
    def get_ads_list(self, multiple_selector: str) -> List:
        return self._find_elements_by_xpath(multiple_selector)
