import os
import time
import pickle
import datetime
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window

# Path to chromedriver executable
current_path = os.getcwd()
chrome_path = os.path.join(current_path, "chromedriver.exe")

# Global variables to store job data
GFG_jobs = []
Unstop_jobs = []
Naukri_jobs = []
job_count = 10

# Function to scrape jobs from GFG
def GFG_JobSearch():
    a = time.time()
    while time.time() - a < 10:
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
            service = Service(chrome_path)
            
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.get("https://www.geeksforgeeks.org/jobs?ref=ghm")

            wait = WebDriverWait(driver, 30)
            elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "jobs_eachJob__42shr")))

            i = 0
            for element in elements:
                job_title = element.find_element(By.CLASS_NAME, "jobs_designation__fVwb4").text
                company_name = element.find_element(By.CLASS_NAME, "jobs_company_name__vfAr8").text
                experience = element.find_element(By.XPATH, ".//div[contains(@class, 'jobs_job_details__4yWvW')]/div[1]/p").text
                salary = element.find_element(By.XPATH, ".//div[contains(@class, 'jobs_job_details__4yWvW')]/div[2]/p").text
                job_location = element.find_element(By.XPATH, ".//div[contains(@class, 'jobs_job_details__4yWvW')]/div[3]/p").text
                apply_before = element.find_element(By.CLASS_NAME, "jobs_last_date__qZHn2").text

                if job_title:
                    GFG_jobs.append({
                        "Job Title": job_title,
                        "Company Name": company_name,
                        "Experience": experience,
                        "Salary": salary,
                        "Job Location": job_location,
                        "Apply Before": apply_before,
                        "Apply at": "https://www.geeksforgeeks.org/jobs?ref=ghm"
                    })

                i += 1
                if i >= job_count:
                    break

            driver.quit()
            break
        except Exception as e:
            print(f"Failed to load GFG page: {e}")

# Function to scrape jobs from Naukri
def Naukri_JobSearch():
    a = time.time()
    while time.time() - a < 20:
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
            service = Service(chrome_path)
            
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.get("https://www.naukri.com/fresher-jobs")

            wait = WebDriverWait(driver, 30)
            elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "srp-jobtuple-wrapper")))

            i = 0
            for element in elements:
                job_title = element.find_element(By.CSS_SELECTOR, "a.title").text
                job_link = element.find_element(By.CSS_SELECTOR, "a.title").get_attribute("href")
                company_name = element.find_element(By.CSS_SELECTOR, "a.comp-name").text
                experience = element.find_element(By.CSS_SELECTOR, ".exp-wrap .expwdth").text
                salary = element.find_element(By.CSS_SELECTOR, ".sal-wrap .sal").text
                location = element.find_element(By.CSS_SELECTOR, ".loc-wrap .locWdth").text
                job_description = element.find_element(By.CSS_SELECTOR, ".job-desc").text
                post_date = element.find_element(By.CSS_SELECTOR, ".job-post-day").text
                
                Naukri_jobs.append({
                    "Job Title": job_title,
                    "Job Link": job_link,
                    "Company Name": company_name,
                    "Experience": experience,
                    "Salary": salary,
                    "Location": location,
                    "Job Description": job_description,
                    "Post Date": post_date,
                    "Apply at": "https://www.naukri.com/fresher-jobs"
                })

                i += 1
                if i >= job_count:
                    break

            driver.quit()
            break
        except Exception as e:
            print(f"Failed to load Naukri page: {e}")

# Function to scrape jobs from Unstop
def Unstop_JobSearch():
    a = time.time()
    while time.time() - a < 10:
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
            service = Service(chrome_path)

            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.get("https://unstop.com/jobs")

            wait = WebDriverWait(driver, 30)
            elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "single_profile")))

            i = 0
            for element in elements:
                job_title = element.find_element(By.TAG_NAME, "h2").text
                company_name = element.find_element(By.TAG_NAME, "p").text
                impressions = element.find_element(By.CSS_SELECTOR, ".other_fields .seperate_box:nth-child(1)").text
                days_left = element.find_element(By.CSS_SELECTOR, ".other_fields .seperate_box:nth-child(2)").text

                if job_title:
                    Unstop_jobs.append({
                        "Job Title": job_title,
                        "Company Name": company_name,
                        "Impressions": impressions,
                        "Days Left": days_left,
                        "Apply at": "https://unstop.com/jobs"
                    })

                i += 1
                if i >= job_count:
                    break

            driver.quit()
            break
        except Exception as e:
            print(f"Failed to load Unstop page: {e}")

# List of scraping functions
function_list = [GFG_JobSearch, Unstop_JobSearch, Naukri_JobSearch]
threads = []

# Load or scrape job data
files_in_directory = os.listdir()
date_str = datetime.date.today().strftime('%Y-%m-%d')
file_name = f"{date_str}.pkl"

if file_name in files_in_directory:
    with open(file_name, 'rb') as file:
        data = pickle.load(file)
else:
    for func in function_list:
        thread = threading.Thread(target=func)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    data = GFG_jobs + Unstop_jobs + Naukri_jobs
    
    with open(file_name, 'wb') as file:
        pickle.dump(data, file)

print("End of Web Scraping")

# Kivy application
class MyGridLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MyGridLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # Top BoxLayout for dropdown and search button
        top_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)

        # Dropdown for job titles
        self.dropdown_job = DropDown()
        btn = Button(text='Select Job Title', size_hint_y=None, height=40)
        btn.bind(on_release=lambda btn: self.dropdown_job.select(btn.text))
        self.dropdown_job.add_widget(btn)
        unique_job = set()
        for item in data:
            if item["Job Title"] not in unique_job:
                unique_job.add(item["Job Title"])
                btn = Button(text=item["Job Title"], size_hint_y=None, height=40)
                btn.bind(on_release=lambda btn: self.dropdown_job.select(btn.text))
                self.dropdown_job.add_widget(btn)

        self.mainbutton_job = Button(text='Select Job Title', size_hint_x=0.3)
        self.mainbutton_job.bind(on_release=self.dropdown_job.open)
        self.dropdown_job.bind(on_select=lambda instance, x: setattr(self.mainbutton_job, 'text', x))
        top_layout.add_widget(self.mainbutton_job)
        
        # Dropdown for company names
        self.dropdown_company = DropDown()
        btn = Button(text='Select Company Name', size_hint_y=None, height=40)
        btn.bind(on_release=lambda btn: self.dropdown_company.select(btn.text))
        self.dropdown_company.add_widget(btn)
        unique_company = set()
        for item in data:
            if item["Company Name"] not in unique_company:
                unique_company.add(item["Company Name"])
                btn = Button(text=item["Company Name"], size_hint_y=None, height=40)
                btn.bind(on_release=lambda btn: self.dropdown_company.select(btn.text))
                self.dropdown_company.add_widget(btn)
                
        self.mainbutton_company = Button(text='Select Company Name', size_hint_x=0.3)
        self.mainbutton_company.bind(on_release=self.dropdown_company.open)
        self.dropdown_company.bind(on_select=lambda instance, x: setattr(self.mainbutton_company, 'text', x))
        top_layout.add_widget(self.mainbutton_company)
        
        # Dropdown for experience
        self.dropdown_exp = DropDown()
        btn = Button(text='Select Experience', size_hint_y=None, height=40)
        btn.bind(on_release=lambda btn: self.dropdown_exp.select(btn.text))
        self.dropdown_exp.add_widget(btn)
        unique_exp = set()
        for item in data:
            if "Experience" in item.keys() and item["Experience"] not in unique_exp:
                unique_exp.add(item["Experience"])
                btn = Button(text=item["Experience"], size_hint_y=None, height=40)
                btn.bind(on_release=lambda btn: self.dropdown_exp.select(btn.text))
                self.dropdown_exp.add_widget(btn)
                
        self.mainbutton_exp = Button(text='Select Experience', size_hint_x=0.3)
        self.mainbutton_exp.bind(on_release=self.dropdown_exp.open)
        self.dropdown_exp.bind(on_select=lambda instance, x: setattr(self.mainbutton_exp, 'text', x))
        top_layout.add_widget(self.mainbutton_exp)
        
        # Toggle button
        self.toggle_btn = ToggleButton(text='Include', size_hint_x=0.3)
        top_layout.add_widget(self.toggle_btn)

        # Search button
        self.search_btn = Button(text='Search', size_hint_x=0.3)
        self.search_btn.bind(on_release=self.on_search)
        top_layout.add_widget(self.search_btn)

        self.add_widget(top_layout)

        # Text input for displaying results
        self.result_box = TextInput(text='', readonly=True, size_hint=(1, 1))
        self.add_widget(self.result_box)

    def on_search(self, instance):
        toggle_state = self.toggle_btn.state
        result = []
        result_text = ''
        
        selected_element_job = self.mainbutton_job.text
        selected_element_company = self.mainbutton_company.text
        selected_element_exp = self.mainbutton_exp.text
        
        selected = {}
        if selected_element_job != 'Select Job Title':
            selected["Job Title"] = selected_element_job
        if selected_element_company != 'Select Company Name':
            selected["Company Name"] = selected_element_company
        if selected_element_exp != 'Select Experience':
            selected["Experience"] = selected_element_exp
        
        if selected:
            if toggle_state == 'normal':
                if selected_element_job != 'Select Job Title':
                    for item in data:
                        if selected_element_job == item["Job Title"]:
                            result.append(item)
                
                if selected_element_company != 'Select Company Name':
                    for item in data:
                        if selected_element_company == item["Company Name"]:
                            result.append(item)
                
                if selected_element_exp != 'Select Experience':
                    for item in data:
                        if "Experience" in item.keys() and selected_element_exp == item["Experience"]:
                            result.append(item)
                            
            else:
                for item in data:
                    shared_items = {k: selected[k] for k in selected if k in item and selected[k] == item[k]}
                    if shared_items == selected:
                        result.append(item)
        else:
            result = data
            
        if result:
            for item in result:
                for key, value in item.items():
                    result_text += f'{key}: {value}\n'
                result_text += '\n'
            self.result_box.text = result_text
        else:
            self.result_box.text = 'No result.'

class MyApp(App):
    def build(self):
        return MyGridLayout()

if __name__ == '__main__':
    MyApp().run()
