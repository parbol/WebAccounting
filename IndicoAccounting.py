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
import datetime
import dateutil
from dateutil.relativedelta import relativedelta

#Technical stuff
NORMAL = '\033[95m'
OKBLUE = '\033[94m'
GOOD = '\033[92m'
ERROR = '\033[91m'
ENDC = '\033[0m'


#############################################################
def printLog(color, message):

    now = str(datetime.datetime.now())
    print(color + '[' + now + '] ' + message + ENDC)


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
def availableRoom(driver, wait):
    driver.implicitly_wait(3)
    try:
        driver.find_element(By.XPATH, '//i[@class="warning sign icon"]')
        printLog(GOOD, 'There are no rooms available')
        return 0
    except:
        return 1


#############################################################
def makeBooking(driver, wait, date, time1, time2, room, meetingName):
    
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
        return 0
    if not availableRoom(driver, wait):
        return 1
    if not sendConfirm(wait):
        return 0
    if not sendUser(wait):
        return 0
    if not sendCreateBooking(wait, meetingName):
        return 0
    return 2

#############################################################
def processDate(day, N):

    theDay = 0
    if day == 'Sunday':
        theDay = 0
    elif day == 'Monday':
        theDay = 1
    elif day == 'Tuesday':
        theDay = 2
    elif day == 'Wednesday':
        theDay = 3
    elif day == 'Thursday':
        theDay = 4
    elif day == 'Friday':
        theDay = 5
    else:
        theDay = 6

    today = datetime.date.today()
    weekday = today.weekday()
    ndays = (theDay-weekday) % 7
    nextday = today + relativedelta(days=+ndays)
    currentday = nextday
    dates = []
    for i in range(0, N):
        nextD = nextday + relativedelta(weeks=+i)
        stringdate = f'{nextD.day}/{nextD.month}/{nextD.year}'
        dates.append(stringdate)
    return dates


#############################################################
if __name__=='__main__':

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    #driver.maximize_window()
    driver.get("https://indico.ifca.es/rooms/book")
    wait = WebDriverWait(driver, 40)
    printLog(GOOD, 'Please fill in your credentials')
    passa = getpass.getpass(GOOD + "Press enter when ready" + ENDC)

    #List of rules
    rules = [['Tuesday', '19:30', '20:30', 'IFCA/P0-017 - Sala Teresa Rodrigo Anoro (Sala de Juntas)', 'Instrumentation meeting']]
    for i in rules:
        printLog(GOOD, 'Request to make a meeting with title: ' + i[4] + ', in room: ' + i[3] + ' from: ' + i[1] + ' to: ' + i[2])

    while True:

        #Condition to trigger the booking (not implemented yet)

        for rule in rules:
            
            listOfDates = processDate(rule[0], 5)
            
            for date in listOfDates:
            
                status = makeBooking(driver, wait, date, rule[1], rule[2], rule[3], rule[4])
    
                if not status:
                    printLog(ERROR, 'Exiting...')
                    sys.exit()
                if status == 1:
                    printLog(ERROR, 'Meeting already reserved')
        
                printLog(GOOD, 'Meeting was booked successfully')

                driver.get("https://indico.ifca.es/rooms/book")
                wait = WebDriverWait(driver, 40)


    # Close the browser
    driver.quit()


