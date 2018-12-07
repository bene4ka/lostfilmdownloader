import os
import requests
from time import sleep
from selenium import webdriver


class GetTorrent(object):
    def __init__(self, link, loginpassword):
        os.environ['MOZ_HEADLESS'] = '1'
        self.driver = webdriver.Firefox(executable_path=r'.\geckodriver\geckodriver.exe')
        self.navigate(link, loginpassword)

    def navigate(self, link, loginpassword):
        driver = self.driver
        driver.get('https://www.lostfilm.tv/login')
        username = driver.find_element_by_xpath("//input[contains(@class,'email-input text-input')]")
        password = driver.find_element_by_xpath("//input[contains(@class,'password-input text-input')]")
#        username.send_keys("nomadium@mail.ru")
#        password.send_keys("xLOUI8n54P")
        username.send_keys(loginpassword[0])
        password.send_keys(loginpassword[1])
        driver.find_element_by_xpath("//input[contains(@class,'primary-btn sign-in-btn')]").click()

        sleep(5)

        driver.get(link)

        sleep(5)

        parent = driver.current_window_handle
        dlname = '_'.join(link.split('/')[4:7]) + '.torrent'

        sleep(3)

        button = driver.find_element_by_xpath("//div[contains(@class,'external-btn')]")
        button.click()

        sleep(5)

        child = driver.window_handles[1]

        driver.switch_to.window(child)
        link = driver.current_url
        driver.close()
        driver.switch_to.window(parent)
        driver.get(link)

        sleep(60)

        links = driver.find_elements_by_partial_link_text('tracktor')
        dl_link = links[1].get_attribute("href")

        driver.close()

        r = requests.get(dl_link)
        with open(dlname, "wb") as code:
            code.write(r.content)