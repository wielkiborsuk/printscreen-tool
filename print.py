import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


class Shoter(object):
    def init_driver(self, width=1280, height=720):
        options = Options()
        options.add_argument('--headless')

        DRIVER = 'chromedriver'
        driver = webdriver.Chrome(DRIVER, chrome_options=options)
        driver.set_window_size(width, height)
        self.driver = driver
        return driver

    def load_page(self, page, timeout=1):
        self.driver.get(page)
        time.sleep(timeout)

    def next_slide(self, timeout=1):
        action = ActionChains(self.driver)
        action.send_keys(Keys.PAGE_DOWN)
        action.perform()

        time.sleep(timeout)

    def shot(self, count):
        if not os.path.exists('out'):
            os.mkdir('out')
        name = 'out/slide-{:02}.png'.format(count)
        screenshot = self.driver.save_screenshot(name)
        return screenshot

    def get_url(self):
        return self.driver.current_url

    def get_snapshot(self):
        sections = self.driver.find_elements_by_css_selector('section.present')
        if not sections:
            return None
        return sections[-1].get_attribute('innerHTML')

    def exit(self):
        self.driver.quit()


def main():
    shoter = Shoter()
    shoter.init_driver()
    shoter.load_page('https://java-tooling.firebaseapp.com')

    previous = {'url': None, 'content': None}
    current = {'url': shoter.get_url(), 'content': shoter.get_snapshot()}
    count = 1

    while current != previous:
        shoter.shot(count)
        shoter.next_slide()
        count += 1
        previous = current
        current = {'url': shoter.get_url(), 'content': shoter.get_snapshot()}

    shoter.exit()


if __name__ == "__main__":
    main()
