import unittest
from faker import Faker
from helpers import get_driver
from pages import LoginPage
from credentials import credentials, base_url
from pages.group_page import GroupPage

faker = Faker()


class CollTestCase(unittest.TestCase):

    def setUp(self):
        self.driver = get_driver()
        # 1)
        login_page = LoginPage(driver=self.driver, url=base_url)
        login_page.open()
        login_page.wait_for_loading()
        coll_page = login_page.login_with(credentials)
        self.page = coll_page

    def test_task(self):
        # 2)
        coll_page = self.page
        section_name = 'test_{}_section'.format(faker.first_name())
        coll_page.add_section(section_name)

        # 3)
        group_data = {'group_name': 'test_{}_group'.format(faker.first_name()), 'description': '1234567890'}
        coll_page.add_group(group_data)

        # 4)
        group_page = coll_page.navigate_created_group()
        object_page = group_page.add_object('test_{}_object'.format(faker.first_name()))

        # 5)
        images_num = 5
        object_page.upload_images(images_num=images_num)
        self.assertEqual(len(list(object_page.uploaded_images)), images_num)

        # 6)
        object_page.add_artist_from_db(artist_part='Leonardo')
        object_page.add_artist({'first_name': faker.first_name(), 'last_name': faker.last_name()})

        # 7)
        object_page.update_status()
        catalogue_text = faker.sentence()
        object_page.add_catalogue_text(catalogue_text)
        self.assertEqual(object_page.catalogue_text.text, catalogue_text)
        comments = [faker.sentence() for _ in range(2)]
        object_page.add_comments(comments)
        self.assertEqual(object_page.get_comments()[::-1], comments)

        # 8)
        object_page.navigate_to_all_objects()
        all_objects = GroupPage()
        all_objects.remove_default_filters()
        all_objects.add_full_text_search(comments[0])
        all_objects.add_filter('Section', 'is', section_name)
        all_objects.apply_filters()
        self.assertEqual(len(list(all_objects.objects)), 1)

        # 9)
        all_objects.select_object()
        report_name = '{}_report'.format(faker.first_name())
        all_objects.generate_report(
            name=report_name, report_type='Contact Sheet', report_format='Word', fields=('Artist', 'Title'))
        self.assertEqual(all_objects.get_notification_text(), 'Generate report\nReport successfully generated.')

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
