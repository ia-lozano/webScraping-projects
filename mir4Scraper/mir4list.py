# pip install selenium
# pip install webdriver_manager
# pip install 'urllib3<2.0'
# pip install pandas

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

website = 'https://www.xdraco.com/nft/list/'

# Setting up chrome driver
chrome_options = Options()
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get(website)
time.sleep(5)

# Getting the total number of characters published, just in case we need it later
# spoiler: it seems to be not necessary
# Another spoiler: not usefull at all, the list changes literally every second
try:
    total_characters = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.XPATH, '//span[@class="list-bar__total nft"]'))
    )
    total_characters = int(total_characters.text)
except:
    print("Element not found, terminating process")
    driver.quit()

# Rendering all the elements to scrape by clicking "view more" button
while True:
    try:
        view_more = WebDriverWait(driver,30).until(
            EC.presence_of_element_located((By.XPATH, '//button[@class="btn-viewmore"]'))
        )
        view_more.click()
    except:
        print('View more button not found or you scrolled till the bottom')
        break

# Getting the full container of the characters list and a list with all the characters
try:
    full_list = driver.find_element(By.XPATH, '//ul[@class="list-item wrap-card"][2]')
    characters = full_list.find_elements(By.XPATH, './li')
except:
    print('List of character not found, perhaps the site is under maintenance or was updated')

# List for csv later
char_class = []
level = []
power_score = []
rate = []

#
for character in characters:
    try:
        class_string = character.find_element(
            By.XPATH, './a/div/div/div/span').text

        char_class.append(class_string)

        level.append(character.find_element(
            By.XPATH, './a/div/div/div/dl/dd').text)

        power_score.append(int(character.find_element(
            By.XPATH, './a/div/div/div/div[2]/div/dd').text.replace(',', '')))

        rate.append(int(character.find_element(
            By.XPATH, './div/button/em/strong').text.replace(',', '')))

        print(f'Character scraped: {class_string}')

    except:
        print('character attribute not found')
        pass

time.sleep(20)

df = pd.DataFrame({'class':char_class, 'level':level, 'power':power_score, 'price':rate})
df.to_csv('nft_list.csv', index=False)
