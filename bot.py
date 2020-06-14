from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.options import Options
my_url = 'https://datanose.nl/'
chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome('F:\chromedriver_win32\chromedriver.exe',options=chrome_options) #download chrome driver and set here the path or set system variable for chromedriver
driver.get(my_url)
def wait_method(by_type, name_param):          
    timeout = 10  
    try:
        element_present = EC.presence_of_element_located((by_type, name_param))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print ("Timed out waiting for page to load")

wait_method(By.CLASS_NAME,'tile')

login_tile = 5
driver.find_elements_by_class_name('tile')[login_tile].click()

from cryptography.fernet import Fernet
import pickle
#Load the key for the crypto password
with open ('crypto_pass.bin', 'rb') as fp:   key = pickle.load(fp)

crypto_suite = Fernet(key)
with open ('credentials.bin', 'rb') as fp:
    credentials = pickle.load(fp)
    #Unencrypt and decode credentials
    cred = [crypto_suite.decrypt(crendential).decode('utf-8').strip() for crendential in credentials]
    

wait_method(By.ID,'username')
username = driver.find_element_by_id('username')
username.send_keys(cred[0])

wait_method(By.ID,'password')
    
password = driver.find_element_by_id('password')
password.send_keys(cred[1])
password.send_keys(Keys.ENTER)

url2 = "nav#enrolmaster"
xpath_master_enrol = '//a[@href="'+url2+'"]'
wait_method(By.XPATH, xpath_master_enrol)

masters = driver.find_element_by_xpath(xpath_master_enrol)
masters.click()

xpath_radio = "//input[@type='radio']"
wait_method(By.XPATH, xpath_radio)
driver.find_element_by_xpath(xpath_radio).click()



def get_position(driver):    
    uva_text = "selected and you are on the waiting list." 
    xpath_position_uva ="//*[contains(text(), '"+uva_text+"')]"
    wait_method(By.XPATH,xpath_position_uva)
    text_uva_position = driver.find_element_by_xpath(xpath_position_uva).text
    print(text_uva_position)
    position = [int(s) for s in text_uva_position.split() if s.isdigit()][0]
    pos_notif = str("Position: "+str(position+1)+"th")

    print(pos_notif)
    
    return int(position+1)

from win10toast import ToastNotifier
def refresh_and_notify(driver):
    
    driver.refresh()
    pos_notif= get_position(driver)
    position_file = open('position', 'r') 
    pos_file = int(position_file.readlines()[0])
    if pos_file == pos_notif:
        print('No changes, position is:',str(pos_notif))
    else:
        with open('position', 'r') as file:
            data = file.readlines()
        data[0]=str(pos_notif)
        f = open("position", "w")
        f.writelines(data)
        f.close()        
        message = str("New position is " + str(pos_notif))
        subject = "Waiting list at UvA"
        send_email(subject,message)

        toaster = ToastNotifier()
        toaster.show_toast(subject,str(pos_notif),duration=60000,threaded=True)
        driver.refresh()


import smtplib,ssl
import json

def send_email(subject, body, file_emails='email.json'):
    #load the emails from file
    with open(file_emails, 'r') as fp:
        email_data = json.load(fp)
        
    receiver = email_data['receiver']
    sender= email_data['sender']
    smtp_server = email_data['smtp_server']

    gmail_password = cred[2]
   
    message = "Subject: "+subject+'\n \n'+body

    port = 587
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted            
            print (sender,'- Login step next!')
            server.login(sender, gmail_password)
            
            print (sender,'- Login Succesful!')
            server.sendmail(sender, receiver, message)
        print ('Email sent!')
        print('Message:',message)
    except:
        print ('Something went wrong...')


# refresh_and_notify(driver)
#loop
import time
program_starts = time.time()
count_ref = 0
original_time=time.time()
while(True):
    now = time.time()   
    if(int(1+now-program_starts)%30 == 0):
        print("It has been {0} seconds since the loop started".format(now - original_time))
        refresh_and_notify(driver)
        print('times refreshed: ',count_ref)
        count_ref+=1        
        program_starts = time.time()



#reformat code
#Clean read me
#add timeloop
#save position in file
#read position from file
#compare current vs file position
#notif if different
#Encrypted passwords
