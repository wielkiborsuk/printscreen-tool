""" small tool to record web-based presentation to pdf by traversing each slide in order """
import time
import os
import shutil
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import click


class Shoter:
    """ class able to record screenshots from slenium webdriver """

    def __init__(self, width=1920, height=1080):
        """ initialize webdriver object, set browser size to match presentation size """
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')

        driver = 'chromium.chromedriver'
        path = '/snap/bin/chromium.chromedriver'
        driver = webdriver.Chrome(driver, options=options)
        driver.set_window_size(width, height)
        self.driver = driver

    def load_page(self, page, timeout=1):
        """ visit specific page and allow for it to load (timeout) """
        self.driver.get(page)
        time.sleep(timeout)

    def next_slide(self, timeout=1):
        """ go to next slide by simulating PAGE_DOWN press and wait for animations if needed """
        action = ActionChains(self.driver)
        action.send_keys(Keys.PAGE_DOWN)
        action.perform()

        time.sleep(timeout)

    def shot(self, count):
        """ save screenshot to a specific path with slide number suffix """
        if not os.path.exists('out'):
            os.mkdir('out')
        name = 'out/slide-{:02}.png'.format(count)
        screenshot = self.driver.save_screenshot(name)
        return screenshot

    def get_url(self):
        """ expose driver current url to verify if presentation has finished """
        return self.driver.current_url

    def get_snapshot(self):
        """ expose html content of current slide to verify if presentation has finished """
        section = self.driver.find_element(By.CSS_SELECTOR, 'section.present')
        if not section:
            return None
        return section.get_attribute('innerHTML')

    def exit(self):
        """ close/quit driver session """
        self.driver.quit()


@click.command(name='print')
@click.option('--output', '-o', default='out/out.pdf', help='Destination for final pdf file')
@click.option('--geometry', '-g', default='1920x1080', help='browser window size for screenshots')
@click.argument('url', default='http://localhost:8000')
def main(url, output, geometry):
    """ accept presentation url as parameter and record presentation to specific file """
    shutil.rmtree('out', ignore_errors=True)
    os.mkdir('out')

    width, height = [int(n) for n in geometry.split('x')]
    shoter = Shoter(width, height)
    shoter.load_page(url)

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

    subprocess.call(['convert', 'out/*.png', output])


if __name__ == "__main__":
    main() # pylint: disable=no-value-for-parameter
