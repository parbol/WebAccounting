#############################################################
# Whatsapp web accounting                              ######
#############################################################
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import getpass



#############################################################
def setTheTime(wait, time1, time2):

    times = [time1, time2]
    try:
        buttoms = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//input[@aria-autocomplete="list"]')))
        for i, e in enumerate(buttoms):
            e.click()
            e.send_keys(Keys.CONTROL + "a")
            e.send_keys(Keys.DELETE)
            e.send_keys(times[i])
    except:
        return False
    return True

#############################################################
def setTheRoom(wait, room):

    try:
        buttomDate = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="e.g. IT Amphitheatre"]')))
        buttomDate.clear()
        buttomDate.send_keys(room)
    except:
        return False
    return True

#############################################################
def setTheDate(wait, date):

    try:
        buttomDate = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="DD/MM/YYYY"]')))
        buttomDate.clear()
        buttomDate.send_keys(date)
    except:
        return False
    return True

#############################################################
def sendButtom(wait):
    
    try:
        buttom = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="ui primary button"]')))
        buttom.click()
    except:
        return False
    return True

#############################################################
def sendConfirm(wait):
    
    try:
        buttom = wait.until(EC.presence_of_element_located((By.XPATH, '//button[@class="ui green circular icon button"]')))
        buttom.click()
    except:
        return False
    return True

#############################################################
def sendUser(wait):
    
    try:
        buttom = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ui radio checkbox"]')))
        buttom.click()
    except:
        return False
    return True

#############################################################
def sendCreateBooking(wait, meetingName):
    
    try:
        buttom2 = wait.until(EC.presence_of_element_located((By.XPATH, '//textarea[@id="finalfield-reason"]')))
        buttom2.send_keys(meetingName)
        buttom3 = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@form="book-room-form"]')))
        buttom3.click()
    except:
        return False
    return True


#############################################################
def makeBooking(wait, date, time1, time2, room, meetingName):
    
    if not setTheDate(wait, date):
        return 'Bad Date'
    if not setTheTime(wait, time1, time2):
        return 'Bad Times'
    if not setTheRoom(wait, room):
        return 'Bad Room'
    if not sendButtom(wait):
        return 'Bad Confirm Room'
    if not sendConfirm(wait):
        return 'Bad confirm'
    if not sendUser(wait):
        return 'Bad User'
    if not sendCreateBooking(wait, meetingName):
        return 'Bad confirm title'

    return 'Good'


#############################################################
def checkProblem(wait):

    try:
        #buttom2 = wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"icon warning message")]')))
        buttom2 = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="ui icon warning message rb-client-js-modules-bookRoom-___BookRoom-module__message-nothing___tDcD5"]')))
        return 'Not possible'
    except:
        return 'Unknown problem'

#############################################################
if __name__=='__main__':

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    #driver.maximize_window()
    driver.get("https://indico.ifca.es/rooms/book")
    wait = WebDriverWait(driver, 40)
    passa = getpass.getpass("Press enter")

    a = makeBooking(wait, '07/03/2026', '19:00', '20:00', 'IFCA/P0-017 - Sala Teresa Rodrigo Anoro (Sala de Juntas)', 'Reunión grupo de instrumentación')

    #while True:

    #    a = makeBooking(wait, '07/03/2026', '19:00', '20:00', 'IFCA/P0-017 - Sala Teresa Rodrigo Anoro (Sala de Juntas)', 'Reunión grupo de instrumentación')
    
    #    if a == 'Good':
    #        print('Booking done successfully')
    #    elif a == 'Bad confirm title':
    #        reason = checkProblem(wait)
    #        if reason == 'Not possible':
    #            print('Not possible to perform the reservation')
    #        else:
    #            print('Unknown problem')
    #    else:
    #        print('Unknown problem')
    #
    #    driver.get("https://indico.ifca.es/rooms/book")
    #    wait = WebDriverWait(driver, 40)

    
    passa = getpass.getpass("Press enter")


    # Close the browser
    driver.quit()


