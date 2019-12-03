import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Locators:
    NAV_SIGN_IN = "nav-link-accountList"
    USERNAME = "ap_email"
    PASSWORD = "ap_password"
    username = "gulsan.celep@useinsider.com"
    password = "wsxzaq1"
    CONTINUE = "continue"
    SIGN_IN = "signInSubmit"
    SEARCHING = "twotabsearchtextbox"
    search_input = "Samsung"
    PAGINATION = "//*[@id='search']/div[1]/div[2]/div/span[8]/div/span/div/div/ul/li[3]/a"
    PRODUCT = "/html/body/div[1]/div[1]/div[1]/div[2]/div/span[4]/div[1]/div[3]/div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h2/a"
    ADD_TO_LIST = "add-to-wishlist-button"
    WISH_LIST = "//ul[@id = 'atwl-dd-ul']/li[3]"
    VIEW_LIST = "WLHUC_viewlist"
    WISH_LIST_DELETE = "//*[@id='a-autoid-7']/span/input"
    SEARCH_CLICK = "//*[@id='nav-search']/form/div[2]/div/input"
    PAGINATION_TWO_TEXT = "//*[@id='search']/span[2]/h1/div/div[1]/div/div/span[1]"
    IS_WISH_LIST = "//*[@id='search']/span[2]/h1/div/div[1]/div/div/span[1]"
    IS_SEARCHING_PAGE = "https://www.amazon.com/s?k=samsung&ref=nb_sb_noss_2"
    IS_WISH_LIST_DELETE = "//*[@id='item_IQ7YT8R70O9SW']/div[2]/div/div/div"


class Actions:

    def __init__(self, driver):
        self.driver = driver

    def click(self, element, loc):
        try:
            if (loc == "ID"):
                selectedElement = (By.ID, element)
                delay = WebDriverWait(self.driver, 70).until(EC.element_to_be_clickable(selectedElement))
                delay.click()
            else:
                selectedElement = (By.XPATH, element)
                delay = WebDriverWait(self.driver, 50).until(EC.element_to_be_clickable(selectedElement))
                delay.click()
        finally:
            self.driver.quit()

    def input(self, element, input):
        try:
            WebDriverWait(self.driver, 70).until(EC.presence_of_element_located((By.ID, element))) \
                .send_keys(input)
        finally:
            self.driver.quit()

    def is_checking(self, element):
        try:
            selectedElement = self.driver.find_element_by_xpath(element).text
            return selectedElement
        finally:
            self.driver.quit()


class BasePage(object):

    def __init__(self, driver):
        self.driver = driver
        self.Actions_Wait = Actions(driver)


class MainPage(BasePage):

    def is_amazon(self):
        assert "https://www.amazon.com/" in self.driver.current_url

    def click_nav_sign_in(self):
        self.Actions_Wait.click(Locators.NAV_SIGN_IN, "ID")

    def searching(self):
        self.Actions_Wait.input(Locators.SEARCHING, Locators.search_input)

    def searching_click(self):
        self.Actions_Wait.click(Locators.SEARCH_CLICK, "XPATH")


class LoginPage(BasePage):

    def username_write(self):
        self.Actions_Wait.input(Locators.USERNAME, Locators.username)

    def password_write(self):
        self.Actions_Wait.input(Locators.PASSWORD, Locators.password)

    def continue_click(self):
        self.Actions_Wait.click(Locators.CONTINUE, "ID")

    def sign_in(self):
        self.Actions_Wait.click(Locators.SIGN_IN, "ID")


class CategoryPage(BasePage):

    def is_searching_page(self):
        self.assertEqual(Locators.IS_SEARCHING_PAGE, self.driver.current_url)

    def pagination(self):
        self.Actions_Wait.click(Locators.PAGINATION, "XPATH")

    def is_pagination_two(self):
        actual = "17-32 of over 10,000 results for"
        self.assertEqual(self.Actions_Wait.is_checking(Locators.PAGINATION_TWO_TEXT), actual)

    def two_pagination_three_product(self):
        self.Actions_Wait.click(Locators.PRODUCT, "XPATH")


class ProductPage(BasePage):

    def add_to_list(self):
        self.Actions_Wait.click(Locators.ADD_TO_LIST, "ID")

    def wish_list(self):
        self.Actions_Wait.click(Locators.WISH_LIST, "XPATH")

    def is_wish_list(self):
        actual = "1 item added to Wish List"
        self.assertEqual(self.Actions_Wait.is_checking(Locators.IS_WISH_LIST), actual)

    def view_list_show(self):
        self.Actions_Wait.click(Locators.VIEW_LIST, "ID")

    def wish_list_delete(self):
        self.Actions_Wait.click(Locators.WISH_LIST_DELETE, "XPATH")

    def is_wish_list_delete(self):
        actual = "Deleted"
        self.assertEqual(self.Actions_Wait.is_checking(Locators.IS_WISH_LIST_DELETE), actual)


class ObjectCreate(object):

    def __init__(self, driver):
        self.driver = driver
        self.main_page = MainPage(self.driver)
        self.login_page = LoginPage(self.driver)
        self.category_page = CategoryPage(self.driver)
        self.product_page = ProductPage(self.driver)


class AmazonTesting(unittest.TestCase, ObjectCreate):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.amazon.com")
        self.driver.maximize_window()

    def test_Amazon(self):
        print(self.driver.current_url)
        self.main_page.is_amazon()
        self.main_page.click_nav_sign_in()
        self.login_page.username_write()
        self.login_page.continue_click()
        self.login_page.password_write()
        self.login_page.sign_in()
        self.main_page.searching()
        self.main_page.searching_click()
        self.category_page.is_searching_page()
        self.category_page.pagination()
        self.category_page.is_pagination_two()
        self.category_page.two_pagination_three_product()
        self.product_page.add_to_list()
        self.product_page.wish_list()
        self.product_page.is_wish_list()
        self.product_page.view_list_show()
        self.product_page.is_wish_list_delete()
        self.product_page.is_wish_list_delete()

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
