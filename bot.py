from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from cryptography.fernet import Fernet
import pickle

my_url = 'https://datanose.nl/' #site
chrome_options = Options()
chrome_options.add_argument("--headless") #Dont render chrome

driver = webdriver.Chrome('F:\chromedriver_win32\chromedriver.exe',options=chrome_options) #download chrome driver and set here the path or set system variable for chromedriver
driver.get(my_url)#Load wwebsite

def wait_method(by_type, name_param):  
    """"
    Method to wait for some element to appear in the js website.
    by_type: Type of parameter we will use to find the element.
    name_param: Parameter to find the element. 
    """        
    timeout = 10  #How long we wait for the element to appear
    try:
        element_present = EC.presence_of_element_located((by_type, name_param))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print ("Timed out waiting for page to load")

wait_method(By.CLASS_NAME,'tile') #Find all the tiles which link to other sites in the website

login_tile = 5 #tile 5 has the login link to UvA
driver.find_elements_by_class_name('tile')[login_tile].click() #Go to login site.


#Load the key for the crypto password
with open ('crypto_pass.bin', 'rb') as fp:   key = pickle.load(fp)
crypto_suite = Fernet(key) # Object to handle cryptology.
#Load the encrypted credentials from bin file.
with open ('credentials.bin', 'rb') as fp:
    credentials = pickle.load(fp) 
    #Unencrypt and decode credentials
    cred = [crypto_suite.decrypt(crendential).decode('utf-8').strip() for crendential in credentials]
    

wait_method(By.ID,'username') # Wait for username element to appear in login site.
username = driver.find_element_by_id('username')
username.send_keys(cred[0]) #Write the username in the input box

wait_method(By.ID,'password') # Wait for password element to appear in login site.
    
password = driver.find_element_by_id('password')
password.send_keys(cred[1])#Write the password in the input box
password.send_keys(Keys.ENTER) #Submit the fields and login

url2 = "nav#enrolmaster" # href with info related to masters application
xpath_master_enrol = '//a[@href="'+url2+'"]' #xpath to find the element we can click and go to enrolmaster
wait_method(By.XPATH, xpath_master_enrol)# Wait for enrolmaster element to appear in main site.

masters = driver.find_element_by_xpath(xpath_master_enrol)
masters.click() #Go to master enrolment site

xpath_radio = "//input[@type='radio']"
wait_method(By.XPATH, xpath_radio)
#Find and click on radio button to load the information of current status in master enrolment
driver.find_element_by_xpath(xpath_radio).click() 



def get_position(driver):    
    """
    Based on text in enrolment website, 
    we extract how many people are before me 
    in the waiting list and return my current position.
    """
    uva_text = "selected and you are on the waiting list."  #Text used to find element
    xpath_position_uva ="//*[contains(text(), '"+uva_text+"')]"
    wait_method(By.XPATH,xpath_position_uva) #Wait for text to load
    text_uva_position = driver.find_element_by_xpath(xpath_position_uva).text
    print(text_uva_position) #Print text with current position for debug purpose.
    #Get the only digit in the text which represents people before me in waiting list.
    position = [int(s) for s in text_uva_position.split() if s.isdigit()][0] 
    pos_notif = str("Position: "+str(position+1)+"th") #debug print position
    print(pos_notif)
    
    return int(position+1) #return my position

from win10toast import ToastNotifier
def refresh_and_notify(driver):    
    driver.refresh() #reload website
    pos_notif= get_position(driver) #get my position 
    position_file = open('position', 'r')  #open file with position from last iteration.
    pos_file = int(position_file.readlines()[0])#get the position number
    if pos_file == pos_notif:#check if i am in a different position
        print('No changes, position is:',str(pos_notif))
    else:
        with open('position', 'r') as file:
            data = file.readlines()  # get lines to rewrite file.
        data[0]=str(pos_notif)  # rewrite position to the new one.
        f = open("position", "w")
        f.writelines(data) #save new position
        f.close()        
        message = str("New position is " + str(pos_notif))
        subject = "Waiting list at UvA"
        send_email(subject,message) #Send an email to myself notifying new position.

        toaster = ToastNotifier() #windows10 notification object
        #create a windows 10 notification
        toaster.show_toast(subject,str(pos_notif),duration=60000,threaded=True)
        driver.refresh() #reload website.


import smtplib,ssl
import json

def send_email(subject, body, file_emails='email.json'):
    #load the emails sender and receiver from file
    with open(file_emails, 'r') as fp:
        email_data = json.load(fp)
        
    receiver = email_data['receiver']
    sender= email_data['sender']
    smtp_server = email_data['smtp_server']
    #get the password for sender email, from previously unencrypted file.  
    gmail_password = cred[2] 
   #Subject: declares subject in email, breakline to define body.
    message = "Subject: "+subject+'\n \n'+body

    port = 587 #port for secure ssl gmail communication.
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  
            server.starttls(context=context)
            server.ehlo()              
            print (sender,'- Login step next!')
            server.login(sender, gmail_password) #login           
            print (sender,'- Login Succesful!')
            server.sendmail(sender, receiver, message) #send message
        print ('Email sent!')
        print('Message:',message)
    except:
        print ('Something went wrong...')



#############################################
######   MAIN LOOP ##########################
#############################################
import time

crash_counter = 0
def loop():
    try:
        program_starts = time.time()
        count_ref = 0
        original_time=time.time()
        check_interval = 30 #seconds interval 
        #check every 30 seconds if position changed.
        while(True):
            now = time.time()   
            if(int(1+now-program_starts)%check_interval == 0):
                print("It has been {0} seconds since the loop started".format(now - original_time))
                refresh_and_notify(driver) #Reload site and notify if new position
                print('times refreshed: ',count_ref)
                count_ref+=1  #track how many times we have checked
                program_starts = time.time() #restart timer.
    except KeyboardInterrupt:
        raise
    except:
        global crash_counter
        crash_counter+=1        
        print("Crash counter: ", crash_counter)
        loop()
loop()


#reformat code
#Clean read me
#add timeloop
#save position in file
#read position from file
#compare current vs file position
#notif if different
#Encrypted passwords
