from selenium.webdriver.common.by import By
from webium import Find, Finds
from .base_page import BasePage
from .object_page import ObjectPage


class GroupPage(BasePage):

    add_object_btn_xpath = '//button[contains(., "Add Object")]'
    create_object_btn = Find(by=By.XPATH, value='//button[contains(., "Create Object")]')
    more_btn = Find(by=By.XPATH, value='//button[contains(., "More")]')
    remove_filter_btn = Find(value='.filter-item .fa-times-circle')
    add_filter_btn = Find(by=By.XPATH, value='//div[contains(., "Add filter")]/i')
    filter_name_xpath = '//label[starts-with(normalize-space(),"{}")]/input'
    filter_btn_xpath = '//div[@class="btn-inner"][contains(., "{}")]'
    filter_options_btn = Find(value='.filter-options-i a')
    filter_option_xpath = '//div[@role="option"][normalize-space()="{}"]'
    filter_value_field = Find(value='form input[name=value]')
    form_update_btn = Find(value='form button')
    apply_filters_btn = Find(by=By.XPATH, value='//button[contains(., "Apply Filters")]')
    objects_css = '.ember-table-table-scrollable-wrapper a[href*=object]'
    objects = Finds(value=objects_css)
    filter_input = Find(value='input[placeholder=Filter]')
    spinner_css = '.spinner'
    object_checkbox = Find(value='.btn-checkmark')
    actions_btn = Find(by=By.XPATH, value='//button[contains(., "Actions")]')
    generate_report_btn = Find(by=By.XPATH, value='//a[contains(., "Generate Report")]')
    search_result_xpath = '//div[contains(@class, "select2-result")][starts-with(normalize-space(),"{}")]'
    notification_css = '.notification'

    def add_object(self, object_title):
        self.wait_for_element_to_be_clickable(element={'type': 'xpath', 'value': self.add_object_btn_xpath})
        add_object_btn = Find(by=By.XPATH, value=self.add_object_btn_xpath, context=self)
        add_object_btn.click()
        object_title_field = self.get_input_by_label('Title')
        self.clear_send_keys(object_title_field, object_title)
        self.create_object_btn.click()
        self.wait_for_loading()
        self.wait_for_ember()
        return ObjectPage()

    def remove_default_filters(self):
        self.wait_for_invisibility_of_element(element={'type': 'css', 'value': self.spinner_css})
        self.more_btn.click()
        self.remove_filter_btn.click()
        self.wait_for_loading()

    def add_full_text_search(self, text_to_search):
        self.clear_send_keys(self.filter_input, text_to_search)

    def add_filter(self, name, _filter, value):
        self.add_filter_btn.click()
        f = Find(by=By.XPATH, value=self.filter_name_xpath.format(name), context=self)
        f.click()
        inner_btn = Find(by=By.XPATH, value=self.filter_btn_xpath.format(name), context=self)
        inner_btn.click()
        self.filter_options_btn.click()
        filter_option = Find(by=By.XPATH, value=self.filter_option_xpath.format(_filter), context=self)
        filter_option.click()
        self.clear_send_keys(self.filter_value_field, value)
        self.form_update_btn.click()
        self.wait_for_loading()

    def apply_filters(self):
        self.apply_filters_btn.click()
        self.wait_for_invisibility_of_element(element={'type': 'css', 'value': self.spinner_css})

    def select_object(self):
        self.object_checkbox.click()

    def generate_report(self, name, report_type, report_format, fields):
        self.actions_btn.click()
        self.generate_report_btn.click()
        report_name_field = self.get_input_by_label('Report name')
        self.clear_send_keys(report_name_field, name)
        report_type_select = self.get_a_by_label('Report type')
        report_type_select.click()
        report_type = Find(by=By.XPATH, value=self.search_result_xpath.format(report_type), context=self)
        report_type.click()

        report_format_select = self.get_a_by_label('Report format')
        report_format_select.click()
        report_format = Find(by=By.XPATH, value=self.search_result_xpath.format(report_format), context=self)
        report_format.click()

        report_fields_input = self.get_input_by_label('Report Fields')

        for field in fields:
            report_fields_input.click()
            field = Find(by=By.XPATH, value=self.search_result_xpath.format(field), context=self)
            field.click()

        self.form_update_btn.click()
        self.wait_for_loading()

    def get_notification_text(self):
        return Find(value=self.notification_css, context=self).text
