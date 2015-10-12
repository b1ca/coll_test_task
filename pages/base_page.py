from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webium import BasePage as WebiumBasePage, Find
from local_webium_settings import implicit_timeout


class BasePage(WebiumBasePage):

    add_btn = Find(by=By.XPATH, value='//form//button|//a[contains(.,"Add")]')
    input_label_xpath = '//form//label[contains(., "{}")]/following::input[1]'
    a_label_xpath = '//form//label[contains(., "{}")]/following::a[1]'
    ember_app_css = '.ember-application'

    objects_link = Find(by=By.XPATH, value='//a[contains(., "Objects")]')
    all_objects_link = Find(by=By.XPATH, value='//a[contains(., "All Objects")]')

    @staticmethod
    def clear_send_keys(element, value):
        element.clear()
        element.send_keys(value)

    def wait_for_loading(self, seconds=180):
        wait = WebDriverWait(self._driver, seconds)
        wait.until(lambda x: self._driver.execute_script('return jQuery.active == 0') is True)

    def wait_for_ember(self, seconds=180):
        wait = WebDriverWait(self._driver, seconds)
        wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, self.ember_app_css)))

    def wait_for_invisibility_of_element(self, **kwargs):
        kwargs['condition'] = ec.invisibility_of_element_located
        self._default_wait(**kwargs)

    def wait_for_visibility_of_element(self, **kwargs):
        kwargs['condition'] = ec.visibility_of_element_located
        self._default_wait(**kwargs)

    def wait_for_element_to_be_clickable(self, **kwargs):
        kwargs['condition'] = ec.element_to_be_clickable
        self._default_wait(**kwargs)

    def _default_wait(self, **kwargs):
        assert kwargs.get('condition') and kwargs.get('element')
        selectors = {
            'css': By.CSS_SELECTOR,
            'xpath': By.XPATH
        }
        el = (selectors.get(kwargs.get('element')['type']), kwargs.get('element')['value'])

        self._driver.implicitly_wait(2)
        wait = WebDriverWait(self._driver, kwargs.get('seconds', 30))
        wait.until(kwargs.get('condition')(el))
        self._driver.implicitly_wait(implicit_timeout)

    def get_input_by_label(self, label):
        return Find(by=By.XPATH, value=self.input_label_xpath.format(label), context=self)

    def get_a_by_label(self, label):
        return Find(by=By.XPATH, value=self.a_label_xpath.format(label), context=self)
