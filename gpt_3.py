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

chrome_opt = uc.ChromeOptions()
prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
chrome_opt.add_experimental_option("prefs", prefs)
driver = uc.Chrome(options=chrome_opt, executable_path=r'C:\path\to\chromedriver.exe')

url = 'https://chat.openai.com/auth/login'
driver.get(url)
buttons = driver.find_elements(By.CLASS_NAME, 'btn-primary')
first_button = buttons[0]
first_button.click()

wait = WebDriverWait(driver, 100)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'input')))

email_input = driver.find_elements(By.CLASS_NAME, 'input')[0]
email_input.send_keys("")
continue_btn = driver.find_elements(By.CLASS_NAME, '_button-login-id')[0]
continue_btn.click()

wait.until(EC.presence_of_element_located((By.ID, 'password')))

password_input = driver.find_element(By.ID, 'password')
password_input.send_keys("")
continue_btn = driver.find_elements(By.CLASS_NAME, '_button-login-password')[0]
continue_btn.click()

wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'btn-neutral')))
next_btn = driver.find_element(By.CLASS_NAME, 'btn-neutral')
next_btn.click()

wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'btn-neutral')))
next_btn = driver.find_elements(By.CLASS_NAME, 'btn-neutral')
next_btn[1].click()

wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'btn-primary')))
done_btn = driver.find_elements(By.CLASS_NAME, 'btn-primary')
done_btn[1].click()

wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'btn-primary')))
done_btn = driver.find_elements(By.CLASS_NAME, 'btn-primary')

wait.until(EC.presence_of_element_located((By.ID, 'prompt-textarea')))
text_area = driver.find_elements(By.ID, 'prompt-textarea')

case_dir = str(os.getcwd()) + "\Cases"
# print(case_dir)
dict_nurse={}
list_of_dirs=[]
new_chat=driver.find_element(By.XPATH,'//*[@id="__next"]/div[1]/div[1]/div/div/div/nav/div[1]/a')
list_of_questions=["What is the Case No. Only output the Case No.?Limit answer to 200 characters",
                   "Which court decided the Case? Only output the Court name.Limit answer to 200 characters",
                   "When was the case decided by the court? Only output the date.Limit answer to 200 characters"]
                #    "When was the case filed with the court?Only output the date.Limit answer to 200 characters",
                #    "Name of the judge who decided the dispute?Only output the name.Limit answer to 200 characters",
                #    "Subject matter of the dispute? Choose from Consumer,Commercial,Securities,Labor,Construction,Maritime,Other.Limit answer to 200 characters",
                #    "Subject matter of the dispute? Choose from Consumer,Commercial,Securities,Labor,Construction,Maritime,Other.If the Subject matter is Other,please mention the subject matter concerned.Limit answer to 200 characters",
                #    "Was a governmental agency/foreign government involved in the dispute?Answer in yes or no.Limit answer to 200 characters",
                #    "If a governmental agency/foreign government was involved in the dispute,output the name of the agency/foreign government involved or output None.Limit answer to 200 characters",
                #    "Was emergency arbitration involved?Only output Yes,No or Can't determine.Limit answer to 200 characters",
                #    "Does the order make a reference to a third-party funder?Only output Yes or No.Limit answer to 200 characters",
                #    "Does the order make a reference to a third-party funder?If the answer is yes,please mention the name of the third-party funder or output None.Limit answer to 200 characters",
                #    "Has an arbitration proceeding commenced in the dispute?Only output Yes,No or Can't determine.Limit answer to 200 characters",
                #    "Was the arbitration proceeding an expedited one?Only output Yes,No or Can't determine.Limit answer to 200 characters",
                #    "How many arbitrators were involved?Only output the number.Limit answer to 200 characters.",
                #    "Name of arbitrators,if mentioned.Limit answer to 200 characters"
                   
                #    ]

# list_of_questions=[
#     "What is the subject matter of the dispute?Select 1 from below\n1)Consumer\n2)Commercial\n3)Securities\n4)Labor\n5)Contruction\n6)Maritime\n7)Bankruptcy\n8)Other\n"
# #     "",
# #     "",
# #     "",
# #     "",
# #     "",
# ]

num_of_questions=len(list_of_questions)
file_paths = os.listdir(case_dir)
# print("File paths:" + str(file_paths))
for file_path in file_paths:
    file_length=0
    with open(case_dir + "/" + file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
        file_length=len(text)
        file.close()
    for num,question in enumerate(list_of_questions):
        answer_text = ''
        if len(text)<30000:
            var_text = question + "\n\n" + text
            pyperclip.copy(var_text)
            text_area[0].send_keys(Keys.CONTROL + 'v')
            submit_btn = driver.find_elements(By.XPATH,  '//*[@id="__next"]/div[1]/div[2]/div/main/div[3]/form/div/div/  button')
            submit_btn[0].click()
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(10)

            groups = driver.find_elements(By.CLASS_NAME, 'group')[-1]
            p_tag = driver.find_elements(By.CSS_SELECTOR, 'p')
            current_answer_text = '' 
            current_answer_text=p_tag[-2].text
            if current_answer_text == '':
                new_chat.click()
                time.sleep(2)
            else:
                answer_text = current_answer_text
                # break
        else:
            number_of_times=len(text)/30000
            remaining_tokens=len(text)
            for i in range(number_of_times-1):
                var_text = question + "\n\n" + text[:]
                pyperclip.copy(var_text)
                text_area[0].send_keys(Keys.CONTROL + 'v')
                submit_btn = driver.find_elements(By.XPATH, '//*[@id="__next"]/div[1]/div[2]/div/main/div[3]/form/div/div/      button')
                submit_btn[0].click()
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(10)

                groups = driver.find_elements(By.CLASS_NAME, 'group')[-1]
                p_tag = driver.find_elements(By.CSS_SELECTOR, 'p')
                current_answer_text = '' 
                current_answer_text=p_tag[-2].text
                if current_answer_text == '':
                    new_chat.click()
                    time.sleep(2)
                else:
                    answer_text = current_answer_text
                # break
                        
        list_of_dirs.append({"question": question,"answer":answer_text})
        
        
        

    print(list_of_dirs)
    print("Sleeping for 100 seconds")
    time.sleep(100)
    