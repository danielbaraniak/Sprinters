from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.service import Service as BraveService

from random import randint

class SprintersDriver:
    def __init__(self) -> None:
        browser = randint(1, 3)
        try:
            if browser == 1:
                self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
            elif browser == 2:
                self.driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
            elif browser == 3:
                self.driver = webdriver.Chrome(service=BraveService(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()))
        except Exception as err:
            print(err)