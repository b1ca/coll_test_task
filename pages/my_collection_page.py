from selenium.webdriver.common.by import By
from webium import Find
from .base_page import BasePage
from .group_page import GroupPage


class MyCollectionPage(BasePage):
    _sections = []
    _groups = []

    add_section_btn = Find(by=By.XPATH, value='//button[contains(., "Add Section")]')
    add_group_btn_xpath = '//div[@class="subtitle"][contains(., "{}")]//button[contains(., "Add Group")]'
    created_group_btn_xpath = '//div[@class="subtitle"][contains(., "{}")]/following::a[contains(., "{}")]'
    group_form_xpath = '//form[contains(., "Add Group")]'

    def add_section(self, section_name):
        self.add_section_btn.click()
        section_name_field = self.get_input_by_label('Section Name')
        self.clear_send_keys(section_name_field, section_name)
        self.add_btn.click()
        self._set_section(section_name)

    def _set_section(self, section_name):
        self._sections.append(section_name)

    def add_group(self, group_data):
        add_group_btn = Find(by=By.XPATH, value=self.add_group_btn_xpath.format(self._sections[-1]), context=self)
        add_group_btn.click()
        group_name_field = self.get_input_by_label('Group Name')
        self.clear_send_keys(group_name_field, group_data.get('group_name'))
        description_field = self.get_input_by_label('Description')
        self.clear_send_keys(description_field, group_data.get('description'))
        self.add_btn.click()
        self._set_group(group_data.get('group_name'))
        self.wait_for_invisibility_of_element(element={'type': 'xpath', 'value': self.group_form_xpath})

    def _set_group(self, group_name):
        self._groups.append(group_name)

    def navigate_created_group(self):
        created_group_btn_xpath = self.created_group_btn_xpath.format(self._sections[-1], self._groups[-1])
        created_group_btn = Find(
            by=By.XPATH, value=created_group_btn_xpath, context=self)
        created_group_btn.click()
        self.wait_for_loading()
        self.wait_for_ember()
        return GroupPage()
