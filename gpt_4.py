import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc
import PyPDF2
import os
from PyPDF2 import PdfReader
import pyperclip
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import csv
import math
from selenium.webdriver.common.action_chains import ActionChains
import pyperclip
import configparser


# Instantiating undetected chromedriver for avoiding CloudFlare verification while logging in chatgpt
chrome_opt = uc.ChromeOptions()
prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
chrome_opt.add_experimental_option("prefs", prefs)
driver = uc.Chrome(options=chrome_opt, executable_path=r'C:\path\to\chromedriver.exe')

# Need this to be able to hover over anything
actions = ActionChains(driver)
wait = WebDriverWait(driver, 100)

# Reading config file where username and password are stored
config = configparser.ConfigParser()
config.read('config.ini')

# File path of the .txt file from where the questions are imported
file_path = './questions.txt' 
with open(file_path, 'r') as file:
    questions = str(file.read())


# Function to open another chrome browser instance and obtain the document link after uploading pdf file and then 
# closing the browser instance
def ask_your_pdf(file_path):
    
    # Instantiating another browser instance for this function named driver1
    chrome_opt = uc.ChromeOptions()
    prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
    chrome_opt.add_experimental_option("prefs", prefs)
    driver1 = uc.Chrome(options=chrome_opt, executable_path=r'C:\path\to\chromedriver.exe')
    url1 = 'https://askyourpdf.com/upload'
    driver1.get(url1)
    
    # For hovering in driver1
    actions = ActionChains(driver1)
    wait = WebDriverWait(driver1, 100)
   
    # Path of the element that takes pdf as input
    input_element = driver1.find_element(By.XPATH, '//*[@id="root"]/div/section/main/main/div[2]/div/span/div[1]/span/input')
    # Sending the file path to the input element 
    input_element.send_keys(file_path)
    # Waiting till the presence of the copy button is detected
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'sc-dXNlpb')))
    time.sleep(4)
    # Getting the link text from the popup after the presence of the copy button is detected
    share_link_text = driver1.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/div/div[2]/div[1]/div/div/span').text
    # Closing driver1
    driver1.close()
    # Returning the link text i.e doc id
    return share_link_text

# Function for logging into ChatGPT by taking login credentials from the config file
def chatgpt_homepage():
    url = 'https://chat.openai.com/auth/login'
    driver.get(url)
    # Locating the Login button
    buttons = driver.find_elements(By.CLASS_NAME, 'btn-primary')
    first_button = buttons[0]
    first_button.click()
    # Waiting till the email input is available
    wait = WebDriverWait(driver, 100)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'input')))
    # Located the email input and saved it into email_input
    email_input = driver.find_elements(By.CLASS_NAME, 'input')[0]
    # Sent email id as key from the config file
    email_input.send_keys(config.get('Credentials', 'username'))
    # Located continue and clicked to continue
    continue_btn = driver.find_elements(By.CLASS_NAME, '_button-login-id')[0]
    continue_btn.click()
    # Waiting for the password input element to be available on the webpage
    wait.until(EC.presence_of_element_located((By.ID, 'password')))
    # Located the password input and saved it into password_input
    password_input = driver.find_element(By.ID, 'password')
    # Sending password from config file to password_input
    password_input.send_keys(config.get('Credentials', 'password'))
    # Locate and click continue to log in
    continue_btn = driver.find_elements(By.CLASS_NAME, '_button-login-password')[0]
    continue_btn.click()
    # Wait till the next button is located,then click the next button
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'btn-neutral')))
    next_btn = driver.find_element(By.CLASS_NAME, 'btn-neutral')
    next_btn.click()
    # Wait till the next button is located,then click the next button
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'btn-neutral')))
    next_btn = driver.find_elements(By.CLASS_NAME, 'btn-neutral')
    next_btn[1].click()
    # Wait till the done button is located,then click the done button
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'btn-primary')))
    done_btn = driver.find_elements(By.CLASS_NAME, 'btn-primary')
    done_btn[1].click()
    
# Function for sending questions to the text area and click submit button
def start_querying(share_link_text):
    print("started querying")
    # Wait till the text area is located
    wait.until(EC.presence_of_element_located((By.ID, 'prompt-textarea')))
    text_area = driver.find_elements(By.ID, 'prompt-textarea')
    # Combining doc id and questions
    input_text = share_link_text+"\n\n"+"Answer these 9 questions:"+"\n"+questions
    # Copying the combined text and pasting it into the text area
    pyperclip.copy(input_text)
    text_area[0].send_keys(Keys.CONTROL + 'v')
    # Locating the submit button and clicking it to get the answer
    submit_btn = driver.find_elements(By.XPATH,'//*[@id="__next"]/div[1]/div[2]/div/main/div[3]/form/div/div/button')
    submit_btn[0].click()
    
# Function to refresh the page
def refresh():
    driver.refresh()
    
# Function to switch to GPT-4 from GPT-3.5
def change_to_gpt4():
    time.sleep(3)
    # changed is for checking if it has been switched to GPT-4 or not,if not then it is calling the function again
    changed=0
    gpt4_btn = driver.find_elements(By.CSS_SELECTOR,'button')
    for btn in gpt4_btn:
        if btn.text=="GPT-4":
            btn.click()
            # Used for hovering over the button named GPT-4
            actions.move_to_element(btn).perform()
            changed=1
    if changed==0:
        change_to_gpt4()
    # Finding plugins
    plugin = driver.find_elements(By.CLASS_NAME, 'truncate')
    for plug in plugin:
        if plug.text=='Plugins':
            plug.click()
    # Finding "No plugins enabled button"
    all_btns = driver.find_elements(By.CSS_SELECTOR,'button')
    for btn in all_btns:
        if btn.text=='No plugins enabled':
            btn.click()
    # Finding the plugin named AskYourPDF and selecting it
    all_li = driver.find_elements(By.CSS_SELECTOR,'li')
    for li in all_li:
        if li.text=="AskYourPDF":
            li.click()
            
# Function to store the answer into a text file
def get_answers(file_name):
    groups = driver.find_elements(By.CLASS_NAME,'group')
    # Need a directory named Answers
    with open("./Answers/{}.txt".format(file_name), "w") as file:
        file.write(groups[-1].text)
    
# Main function
def main():
    # Storing the directory path to case_dir
    # Need a directory named West Cases
    case_dir = str(os.getcwd()) + "\West_Cases"
    # Storing the list of files to file_paths
    file_paths = os.listdir(case_dir)
    # Calling the function for opening chatgpt homepage
    chatgpt_homepage()
    # Calling the function for changing gpt 3.5 to gpt 4.0
    change_to_gpt4()
    # Iterating through all the files in the directory
    for file in file_paths:
        # Gettin the doc id for each file from a function named ask_your_pdf and storing it in share_link_text
        share_link_text=ask_your_pdf(case_dir + "/" + file)
        time.sleep(5)
        # Calling the function to start sending questions to chatgpt
        start_querying(share_link_text)
        # Sleeping for 300 seconds to wait for chatgpt to output the answer
        time.sleep(300)
        # Calling the function for copying the answer from the chat
        get_answers(file)
        time.sleep(2)
        # driver.refresh() is for refreshing the page
        driver.refresh()
    
main()

driver.quit()
