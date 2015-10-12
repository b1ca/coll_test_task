from webium import Find
from .base_page import BasePage
from .my_collection_page import MyCollectionPage


class LoginPage(BasePage):

    username_field = Find(value='div.login input')
    password_field = Find(value='div.password input')
    sign_in_btn = Find(value='button')

    def login_with(self, credentials):
        self.clear_send_keys(self.username_field, credentials.get('username'))
        self.clear_send_keys(self.password_field, credentials.get('password'))
        self.sign_in_btn.click()
        self.wait_for_ember()
        return MyCollectionPage()
