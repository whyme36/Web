from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#get website by driver chrome
driver = webdriver.Chrome('./chromedriver')
driver.get("https://orteil.dashnet.org/cookieclicker/")

#look for elements (it can be done in a simpler way driver.find_element_by_xpath('//*[@id="bigCookie"]')
#but to prevent errors that occur when a page does not load fully, I used the function WebDriverWait to delay
try:
    cookie = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="bigCookie"]')))
    cookie_count = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="cookies"]')))
except:
    driver.quit()

#create Action chain click()
actions=ActionChains(driver)
actions.click(cookie)

#infinity loop of clicking on cookie and adding products if costs is;t to big
while True:
    actions.perform()
    coockie_count_find=re.compile(r'\d+')
    count=int(re.findall(coockie_count_find, cookie_count.text)[0])
    try:
        items = [WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'product' + str(i)))) for i in range(1, -1, -1)]
    except:
        driver.quit()
    for item in items:
        value_of_product= int(re.findall(coockie_count_find,item.text)[0])
        if value_of_product <=count:
            product=ActionChains(driver)
            product.move_to_element(item)
            product.click()
            product.perform()



