# Auto Almost Everything
# Youtube Channel https://www.youtube.com/channel/UC4cNnZIrjAC8Q4mcnhKqPEQ
# Facebook Community https://www.facebook.com/loveAAEmuch
# Github Source Code https://github.com/srcAAE?tab=repositories
# Please read README.md carefully before use

import random
import threading
import time

from selenium.webdriver.common.keys import Keys  # python -m pip install selenium
from win10toast import ToastNotifier  # python -m pip install win10toast

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chromedriver_path = '.\\chromedriver.exe'  # <-- Change to your Chrome WebDriver path, replace "\" with "\\".
opts = Options()
opts.binary_location = 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'  # <-- Change to your Chromium browser path, replace "\" with "\\".
opts.add_experimental_option('excludeSwitches', ['enable-automation'])
opts.add_experimental_option('useAutomationExtension', False)


# Notification
def Notification(app, content):
    try:
        toast = ToastNotifier()
        toast.show_toast(app, content, duration=6)
    except:
        pass


sync = True


# Search 30 times per hour
def PreSearch():
    app = 'PreSearch'
    path = 'https://engine.presearch.org'
    presearch_cookies = [
        {
            'name': 'remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d',
            # Replace by your remember token -->
            'value': 'YourRememberTokenHere',
            # <-- Replace by your remember token
            'domain': '.presearch.org',
            'path': '/',
        },
        {
            'name': 'token',
            # Replace by your token -->
            'value': 'YourTokenHere',
            # <-- Replace by your token
            'domain': '.presearch.org',
            'path': '/',
        },
    ]
    word_site = 'https://www.mit.edu/~ecprice/wordlist.10000'
    response = requests.get(word_site)
    word_list = response.content.splitlines()
    presearch_max_count = 30

    while True:
        global sync
        if sync:
            sync = False
            browser = webdriver.Chrome(options=opts, executable_path=chromedriver_path)
            browser.set_page_load_timeout(60)
            try:
                browser.get(path)
                time.sleep(1)
                for cookie in presearch_cookies:
                    browser.add_cookie(cookie)
                browser.get(path)
                time.sleep(1)
                count = 0
                while True:
                    browser.get(path)
                    time.sleep(3)
                    q = ' '.join(
                        [word_list[random.randint(0, len(word_list))].decode() for j in range(random.randint(1, 6))])
                    try:
                        browser.find_element_by_xpath("//input[@placeholder='Search']").send_keys(q, Keys.ENTER)
                        time.sleep(3)
                        if 'Oops, something went wrong with your search' not in browser.page_source and 'The request could not be satisfied' not in browser.title:
                            for i in range(random.randint(1, 3)):
                                try:
                                    results = browser.find_elements_by_xpath(
                                        "//h3[@class='font-semibold text-lg text-primary-600 transition duration-150 hover:underline hover:opacity-70 dark:hover:opacity-60 dark:text-blue-200 dark:font-normal']")
                                    results[random.randint(0, len(results) - 1)].click()
                                    time.sleep(3)
                                    browser.back()
                                    time.sleep(3)
                                except:
                                    pass
                            count += 1
                    except:
                        pass
                    if count > presearch_max_count * 120 / 100:
                        Notification(app, 'Searched 30 times!')
                        break
                    time.sleep(12)
            except Exception as ex:
                print('%s has exception:\n%s!' % (app, ex))
                Notification(app, '%s has exception:\n%s!' % (app, ex))
            finally:
                browser.quit()
            sync = True
            time.sleep(7200)
        else:
            time.sleep(1)


try:
    threads = []
    threads.append(threading.Thread(target=PreSearch, args=()))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
except Exception as ex:
    print('Threading has exception:\n%s!' % ex)

# Please Like Facebook, Subscribe to Youtube channel, Give stars to Git repositories to support us!
# Contact me: autoalmosteverything.2021@gmail.com
