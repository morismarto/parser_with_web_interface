from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from selenium.webdriver import Chrome
import time
from pprint import pprint
from typing import List

class Parser:

    __products_descr = None

    def __init__(self, url: str, stealth_mode: bool = False, sleep: float = None, log_level: int = 1, headless: bool = False) -> None:
        self.__url = url
        self.__sleep = sleep
        self.__headless = headless
        self.__stealth_mode = stealth_mode
        self.__chrome = webdriver.Chrome
        self.__chrome_opt = webdriver.ChromeOptions()
        self.__log_level = log_level

    @property
    def url(self) -> str:
        return self.__url

    @classmethod
    def length_product_descr(cls) -> int:
        return len(cls.__products_descr)

    @classmethod
    def get_data(cls) -> List[str]:
        return cls.__products_descr

    def __set_headless_mode(self) -> None:
        self.__chrome_opt.add_argument("--headless=new")

    def __set_time_sleep(self) -> None:
        time.sleep(self.__sleep)
    
    def __set_log_level(self) -> None:
        self.__chrome_opt.add_argument(f'log-level={self.__log_level}')

    def __set_stealth_opt(self) -> None:
        self.__chrome_opt.add_argument("start-maximized")
        self.__chrome_opt.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.__chrome_opt.add_experimental_option('useAutomationExtension', False)

    def __set_stealth_mode(self, driver: webdriver.Chrome) -> None:
        stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win64",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

    def parse(self) -> None:
        if self.__headless:
            self.__set_headless_mode()
        if isinstance(self.__log_level, int) and (self.__log_level > 0) and (self.__log_level <= 3): 
            self.__set_log_level()
        else:
            raise ValueError('log_level must be int, in the range from 1 to 3')
        self.__set_stealth_opt()
        with self.__chrome(options=self.__chrome_opt) as driver:
            if self.__stealth_mode:
                self.__set_stealth_mode(driver)
            driver.get(self.__url)
            driver.implicitly_wait(10)
            if self.__sleep:
                self.__set_time_sleep()
            self.__handle_page(driver)

    @classmethod
    def __handle_page(cls, driver: Chrome):
        products = driver.find_elements(By.CLASS_NAME, value='product-card')
        cls.__products_descr = [product.find_element(By.TAG_NAME, value='a').get_attribute('aria-label')
         for product in products]
        



if __name__ == '__main__':
    URL = "https://www.wildberries.ru/catalog/0/search.aspx?search=%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE%D0%BA%D0%B0%D1%80%D1%82%D1%8B"
    Parser(url=URL, stealth_mode=True, log_level=3, headless=False).parse()
    pprint(Parser.get_data())
    
