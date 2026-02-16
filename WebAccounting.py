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


#############################################################
def extractNew(oldList, newList):

    Nnew = len(newList)
    if not Nnew:
        return newList
    Nold = len(oldList)
    if not Nold:
        return newList
    newWord = []
    for i in reversed(range(Nnew)):
        isEqual = True
        if newList[i] != oldList[Nold-1] and isEqual:
            newWord.append(newList[i])
        else:
            for j in range(i-1):
                if newList[i-1-j] != oldList[Nold-1-j]:
                    isEqual = False
                    break
        if isEqual == False:
            break
    newWord.reverse()

    return newWord


#############################################################
def process(newMessages):

    print('-------------------New messages:-------------------') 
    for e in newMessages:
        print(e)



#############################################################
if __name__=='__main__':

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    wait = WebDriverWait(driver, 40)
    login_page = LoginPage(driver)
    login_page.load()

    user_name = "Buffer"
    user = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@title="{}"]'.format(user_name))))
    user.click()


    collectionOfMessages = []

    while True:
        message = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class,'copyable-text')]"))) 
        #message = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[@data-testid='selectable-text']"))) 
        newCollectionOfMessages = []
        for i in message:
            #parent = i.parent
            #gparent = parent.parent
            try:
                metadata = i.get_attribute('data-pre-plain-text')
                texto = metadata + ' ' + i.text
                newCollectionOfMessages.append(texto)
            except:
                pass
        newMessages = extractNew(collectionOfMessages, newCollectionOfMessages)
        if len(newMessages) != 0:
            process(newMessages)
            collectionOfMessages.extend(newMessages)
        time.sleep(10)

    # 3. Logout
    header_page = HeaderPage(driver)
    header_page.logout()

    # Close the browser
    driver.quit()


