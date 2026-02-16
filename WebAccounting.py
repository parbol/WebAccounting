#############################################################
# Whatsapp web accounting                              ######
#############################################################
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from simon.accounts.pages import LoginPage
from simon.header.pages import HeaderPage
from simon.pages import BasePage


def newMessages(oldList, newList):

    Nnew = len(newList)
    for i in range(0, Nnew):
        if newList[Nnew-1-i] != oldList[Nold-1]:
            reallyNew.append(Nnew)




if __name__=='__main__':

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    wait = WebDriverWait(driver, 20)
    login_page = LoginPage(driver)
    login_page.load()

    user_name = "Buffer"
    user = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@title="{}"]'.format(user_name))))
    user.click()


    collectionOfMessages = []

    while True:
        message = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='copyable-text']"))) 
        newCollectionOfMessages = []
        for i in message:
            try:
                texto = i.text
                newCollectionOfMessages.append(texto)
            except:
                pass
        newMessages(collectionOfMessages, newCollectionOfMessages)
        time.sleep(10)

    # 3. Logout
    header_page = HeaderPage(driver)
    header_page.logout()

    # Close the browser
    driver.quit()


