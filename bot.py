from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
my_url = 'https://datanose.nl/#'
login ='https://content.datanose.nl/pages/login.jpg'
driver = webdriver.Chrome('F:\chromedriver_win32\chromedriver.exe')
driver.get(my_url)

timeout = 5
try:
    element_present = EC.presence_of_element_located((By.CLASS_NAME, 'tile'))
    WebDriverWait(driver, timeout).until(element_present)
except TimeoutException:
    print ("Timed out waiting for page to load")



titles = driver.find_elements_by_class_name('tile')
login_tile = 5
titles[login_tile].click()


timeout = 5
try:
    element_present = EC.presence_of_element_located((By.ID, 'username'))
    WebDriverWait(driver, timeout).until(element_present)
except TimeoutException:
    print ("Timed out waiting for page to load")


file5 = open('Credentials', 'r') 
Lines = file5.readlines() 

username = driver.find_element_by_id('username')
username.send_keys(Lines[0])
try:
    element_present = EC.presence_of_element_located((By.ID, 'password'))
    WebDriverWait(driver, timeout).until(element_present)
except TimeoutException:
    print ("Timed out waiting for page to load")
    
password = driver.find_element_by_id('password')
password.send_keys(Lines[1])
password.send_keys(Keys.ENTER)
print('end')
print(username)
url2 = "nav#enrolmaster"
try:
    element_present = EC.presence_of_element_located((By.XPATH, '//a[@href="'+url2+'"]'))
    WebDriverWait(driver, timeout).until(element_present)
except TimeoutException:
    print ("Timed out waiting for page to load")

masters = driver.find_element_by_xpath('//a[@href="'+url2+'"]')
masters.click()
print(masters)
print('DONE')

url2 = 'radio'    
timeout = 10
try:    
    element_present = EC.presence_of_element_located((By.XPATH, "//input[@type='radio']"))
    WebDriverWait(driver, timeout).until(element_present)
except TimeoutException:
    print ("Timed out waiting for page to load")
radio = driver.find_element_by_xpath("//input[@type='radio']")
radio.click()
uva_text = "selected and you are on the waiting list." 


try:    
    element_present = EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '"+uva_text+"')]"))
    WebDriverWait(driver, timeout).until(element_present)
except TimeoutException:    
    print ("Timed out waiting for page to load")
texta = driver.find_element_by_xpath("//*[contains(text(), '"+uva_text+"')]")
text_uva_position = texta.text
print(text_uva_position)
position = [int(s) for s in text_uva_position.split() if s.isdigit()][0]
pos_notif = str("Position: "+str(position+1)+"th")

print(pos_notif)
from win10toast import ToastNotifier
toaster = ToastNotifier()
toaster.show_toast("Waiting list at UvA",pos_notif)

driver.refresh()
