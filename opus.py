import sys, time, os, glob
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pyvirtualdisplay import Display

print('Starting OPUS-Selenium...\n')

# Start Virtual Display for headless operation
display = Display(visible=0, size=(1920, 1080)).start()
time.sleep(1)

# Get most recent .obs file
pattern="*.obs" # This pattern may need updated to only search a specific directory
files = list(filter(os.path.isfile, glob.glob(pattern)))
files.sort(key=lambda x: os.path.getmtime(x))
lastfile = files[-1]

# Set configuration variables
myemail = 'YOUREMAILHERE'
antenna_height = 'YOURANTENNAHEIGHT'
file = lastfile

print("Your file is " + file)
print("Your email is " + myemail)
print("Your antenna height is " + antenna_height)

# Set Driver
driver = webdriver.Firefox("/usr/local/bin")
#driver._is_remote = False

# Get OPUS Webpage
driver.get("https://www.ngs.noaa.gov/OPUS/")
assert "OPUS" in driver.title

# Upload File
upload = driver.find_element(by=By.NAME, value="uploadfile")
upload.send_keys(file)
print('File Uploaded Successfully')

# Open Antenna Dropdown to dynamically load content
driver.find_element(by=By.XPATH, value='//*[@id="container"]/form/div[1]/span/span[1]/span/span[2]').click()
print('Dropdown opened')
time.sleep(2)

# Set Antenna Config
actions = ActionChains(driver)
actions.send_keys('SFETOP106').perform()
time.sleep(2)
actions.send_keys(Keys.RETURN).perform()
time.sleep(2)
print('Antenna Selected')

# Set Antenna Height Value
height_object = driver.find_element(by=By.NAME, value="height")
height_object.clear()
time.sleep(1)
height_object.send_keys(antenna_height)
print('Height Entered')
time.sleep(1)

# Set Email Address Value
email = driver.find_element(by=By.NAME, value="email_address")
time.sleep(1)
email.send_keys(myemail)
print('Email Entered')
time.sleep(1)

# Submit File
driver.find_element(by=By.NAME, value="Static").click()
print('Submitted')

#Alert(driver).accept()

sys.exit()