from webium.driver import get_driver as webium_get_driver


def get_driver():
    driver = webium_get_driver()
    driver.set_page_load_timeout(120)
    driver.maximize_window()
    return driver
