import os
from selenium.webdriver.common.by import By
from webium import Find, Finds
from .base_page import BasePage

TABS = ('Description', 'Images', 'Financials', 'Offers', 'Consignments', 'Attachments', 'Locations')


class ObjectPage(BasePage):
    tab_xpath = '//a[.="{}"]'
    active_tab = Find(value='a.active[href]')
    add_photo_btn_css = '.tab-content button'
    add_photo_btn = Find(value=add_photo_btn_css)
    files_input = Find(value='input.files')
    upload_all_btn = Find(by=By.XPATH, value='//button[contains(., "Upload All")]')
    uploaded_images_css = '.scrolled-container img#pic[src]'
    uploaded_images = Finds(value=uploaded_images_css)
    artists_add_btn = Find(by=By.XPATH, value='//h4[.="Artists"]/following::button[1]')
    status_edit_btn = Find(by=By.XPATH, value='//h4[.="Status"]/following::button[1]')
    status_form_xpath = '//form[contains(., "Status")]'
    catalogue_text_form_xpath = '//form[contains(., "Catalogue Text")]'
    catalogue_text_add_btn = Find(by=By.XPATH, value='//h4[.="Catalogue Text"]/following::button[1]')
    catalogue_text_field = Find(
        by=By.XPATH, value='//form[contains(., "Catalogue Text")]//div[contains(@class, "textarea")]')
    catalogue_text = Find(by=By.XPATH, value='//div[@class="subtitle"][contains(.,"Catalogue Text")]/following::div[1]')
    comment_add_btn = Find(by=By.XPATH, value='//h4[.="Comments"]/following::button[1]')
    comment_text_field = Find(by=By.XPATH, value='//form[contains(.,"Add Comment")]//div[contains(@class, "textarea")]')
    comments_xpath = '//div[@class="subtitle"][contains(., "Comments")]/following::ul[1]//div[@id]'
    choice_btn = Find(value='a.select2-choice')
    search_field_css = '.select2-search input'
    search_field = Find(value=search_field_css)
    search_result = Find(value='.select2-results div[role=option]')
    manual_add_artist_btn_css = '.artist-select a.btn'
    manual_add_artist_btn = Find(value=manual_add_artist_btn_css)
    create_btn = Find(by=By.XPATH, value='//a[contains(., "Create")]')
    div_row_xpath = '//div[@class="row"][contains(.,"{}")]'
    form_save_btn_xpath = '//form//button|//a[contains(., "Save")]'
    form_save_btn = Find(by=By.XPATH, value=form_save_btn_xpath)

    def upload_images(self, images_num=1):
        self._activate_tab('Images')
        self.add_photo_btn.click()
        for _ in range(images_num):
            self.files_input.send_keys(os.path.abspath('../img/dog.jpg'))
        self.upload_all_btn.click()
        self.wait_for_loading()
        self.wait_for_visibility_of_element(element={'type': 'css', 'value': self.uploaded_images_css})

    def add_artist_from_db(self, artist_part):
        self._activate_tab('Description')
        self.artists_add_btn.click()
        self.choice_btn.click()
        self.clear_send_keys(self.search_field, artist_part)
        self.wait_for_loading()
        self.search_result.click()
        self.wait_for_invisibility_of_element(element={'type': 'css', 'value': self.manual_add_artist_btn_css})

    def add_artist(self, artist_data):
        self._activate_tab('Description')
        self.artists_add_btn.click()
        self.manual_add_artist_btn.click()
        f_name = self.get_input_by_label('First Name')
        self.clear_send_keys(f_name, artist_data.get('first_name'))
        l_name = self.get_input_by_label('Last Name')
        self.clear_send_keys(l_name, artist_data.get('last_name'))
        self.create_btn.click()
        self.wait_for_invisibility_of_element(element={'type': 'css', 'value': self.manual_add_artist_btn_css})

    def update_status(self):
        self._activate_tab('Description')
        self.status_edit_btn.click()
        self.choice_btn.click()
        self.search_result.click()
        price_field = self.get_input_by_label('Asking Price')
        self.clear_send_keys(price_field, '100')
        net_to_seller_field = self.get_input_by_label('Net To Seller')
        self.clear_send_keys(net_to_seller_field, '50')
        self.form_save_btn.click()
        self.wait_for_invisibility_of_element(element={'type': 'xpath', 'value': self.status_form_xpath})

    def add_catalogue_text(self, text):
        self._activate_tab('Description')
        self.catalogue_text_add_btn.click()
        self.clear_send_keys(self.catalogue_text_field, text)
        self.form_save_btn.click()
        self.wait_for_loading()
        self.wait_for_invisibility_of_element(element={'type': 'xpath', 'value': self.catalogue_text_form_xpath})

    def add_comments(self, comments):
        self._activate_tab('Description')
        for c in comments:
            self.comment_add_btn.click()
            self.clear_send_keys(self.comment_text_field, c)
            self.form_save_btn.click()
            self.wait_for_invisibility_of_element(element={'type': 'xpath', 'value': self.form_save_btn_xpath})

    def get_comments(self):
        comments = Finds(by=By.XPATH, value=self.comments_xpath, context=self)
        return [x.text for x in comments]

    def _activate_tab(self, tab_name):
        assert tab_name in TABS
        if self.active_tab.text != tab_name:
            tab = Find(by=By.XPATH, value=self.tab_xpath.format(tab_name), context=self)
            tab.click()

    def navigate_to_all_objects(self):
        self.objects_link.click()
        self.all_objects_link.click()
