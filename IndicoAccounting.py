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


#Technical stuff
NORMAL = '\033[95m'
OKBLUE = '\033[94m'
GOOD = '\033[92m'
ERROR = '\033[91m'
ENDC = '\033[0m'


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
        printLog(GOOD, 'Time set successfully')
    
    except:
        printLog(ERROR, 'Error setting the time')
        return False
    return True

#############################################################
def setTheRoom(wait, room):

    try:
        buttomDate = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="e.g. IT Amphitheatre"]')))
        buttomDate.clear()
        buttomDate.send_keys(room)
        printLog(GOOD, 'Room set successfully')
    except:
        printLog(ERROR, 'Error setting the room name')
        return False
    return True

#############################################################
def setTheDate(wait, date):

    try:
        buttomDate = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="DD/MM/YYYY"]')))
        buttomDate.clear()
        buttomDate.send_keys(date)
        printLog(GOOD, 'Date set successfully')
    except:
        printLog(ERROR, 'Error setting the date')
        return False
    return True

#############################################################
def sendButtom(wait):
    
    try:
        buttom = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="ui primary button"]')))
        buttom.click()
        printLog(GOOD, 'Search button clicked successfully')
    except:
        printLog(ERROR, 'Error clicking the search button')
        return False
    return True

#############################################################
def sendConfirm(wait):
    
    try:
        buttom = wait.until(EC.presence_of_element_located((By.XPATH, '//button[@class="ui green circular icon button"]')))
        buttom.click()
        printLog(GOOD, 'Confirmation button clicked successfully')
    except:
        printLog(ERROR, 'Error clicking confirmation button')
        return False
    return True

#############################################################
def sendUser(wait):
    
    try:
        buttom = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ui radio checkbox"]')))
        buttom.click()
        printLog(GOOD, 'User selected successfully')
    except:
        printLog(ERROR, 'Error selecting user')
        return False
    return True

#############################################################
def sendCreateBooking(wait, meetingName):
    
    try:
        buttom2 = wait.until(EC.presence_of_element_located((By.XPATH, '//textarea[@id="finalfield-reason"]')))
        buttom2.send_keys(meetingName)
        buttom3 = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@form="book-room-form"]')))
        buttom3.click()
        printLog(GOOD, 'Setting the name of the meeting and clicking was successfull')
    except:
        printLog(ERROR, 'Error setting the name of the meeting and clicking')
        return False
    return True


#############################################################
def makeBooking(wait, date, time1, time2, room, meetingName):
    
    # 0 is unknown error
    # 1 is there are no matches for that time/date
    # 2 is good 
    if not setTheDate(wait, date):
        return 0
    if not setTheTime(wait, time1, time2):
        return 0
    if not setTheRoom(wait, room):
        return 0
    if not sendButtom(wait):
        return 1
    if not sendConfirm(wait):
        return 0
    if not sendUser(wait):
        return 0
    if not sendCreateBooking(wait, meetingName):
        return 0
    return 2


#############################################################
def checkProblem(wait):

    try:
        buttom2 = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="ui icon warning message rb-client-js-modules-bookRoom-___BookRoom-module__message-nothing___tDcD5"]')))
        printLog(GOOD, 'There are no rooms available')
        return 2
    except:
        printLog(ERROR, 'Unexpected error with the check page')
        return 0

#############################################################
if __name__=='__main__':

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    #driver.maximize_window()
    driver.get("https://indico.ifca.es/rooms/book")
    wait = WebDriverWait(driver, 40)
    passa = getpass.getpass("Press enter")


    while True:

        a = makeBooking(wait, '07/03/2026', '19:00', '20:00', 'IFCA/P0-017 - Sala Teresa Rodrigo Anoro (Sala de Juntas)', 'Reunión grupo de instrumentación')
    
        if a == 2:
            printLog(GOOD, 'Meeting was booked')
        elif a == 1:
            reason = checkProblem(wait)

        
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


