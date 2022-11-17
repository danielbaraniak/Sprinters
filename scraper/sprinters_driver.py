from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.service import Service as BraveService
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from scraper_utils import get_random_number_from_range
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from typing import List

class SprintersDriver:
    def __init__(self) -> None:
        browser = 1#get_random_number_from_range(1, 3)
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

    def close_cookies(self, cookies_config_routes: List[str]) -> bool:
        self.driver.implicitly_wait(3)
        which_route = 2#get_random_number_from_range(1, 2)
        try:
            if which_route == 1:
                self.driver.implicitly_wait(1)
                self._find_element_by_id(cookies_config_routes[0]).click()
                return True
            elif which_route == 2:
                self.driver.implicitly_wait(1)
                self._find_element_by_id(cookies_config_routes[1]).click()
                self._find_element_by_class_name(cookies_config_routes[2]).click()
                return True
        except NoSuchElementException as ex:
            print(ex)
            return True
        except ElementClickInterceptedException as ex:
            print(ex)
            return False
        return False
    
    def _move_to_site(self, site: str) -> None:
        self.driver.get(site)
    
    def move_to_next_site(self, pagination_selector: str, pagination_xpath_child: str) -> bool:
        self.driver.implicitly_wait(3) #randomize between 3 and 7
        try:
            href_selector = self._find_element_by_xpath(pagination_selector)
            self.driver.execute_script('window.scrollBy(0, 11000)')
            self._move_to_site(self._find_child_element_by_xpath(href_selector, pagination_xpath_child).get_attribute('href'))
            return True
        except NoSuchElementException as ex:
            print(ex)
            return False
        except ElementClickInterceptedException as ex:
            print(ex)
            return False