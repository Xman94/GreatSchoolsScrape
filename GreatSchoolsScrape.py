from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import csv
import time


# def highlight(element, effect_time, color, border):
#     d = element._parent
#     def apply_style(s):
#         d.execute_script("arguments[0].setAttribute('style', arguments[1]);",
#                               element, s)
#     original_style = element.get_attribute('style')
#     apply_style("border: {0}px solid {1};".format(border, color))
#     time.sleep(effect_time)
#     apply_style(original_style)
# # open_window_elem = driver.find_element_by_id("openwindow")
# # highlight(open_window_elem, 3, "blue", 5)

class GreatSchoolsScrape:
    def __init__(self):
     # Set the path to the ChromeDriver executable
     chrome_driver_path = 'C:\\Users\\Xavier\\Desktop\\Python\\GreatSchoolsScrape\\chromedriver.exe'
    
     # Create a ChromeService object
     service = ChromeService(executable_path=chrome_driver_path)
    
     # Create a ChromeOptions object and set the "no-sandbox" flag
     chrome_options = Options()
     chrome_options.add_argument('--no-sandbox')
    
     # Start the Chrome browser with the "no-sandbox" flag and the ChromeService object
     self.driver = webdriver.Chrome(service=service, options=chrome_options)
    
     # Maximize the window
     self.driver.maximize_window()
     
    def get_address(self):
        self.address = ""
        while self.address == "":
            self.address = input('Please Enter an Address: ')

    def navigate_Greatschools(self):
        self.driver.get('https://www.greatschools.org/')
        print('Navigating to Great Schools')
        WebDriverWait(self.driver, 10)


    def enter_address(self):
        # Locate the address search box and send the address
        print('Submitting the address')
        # Locate the search box element
        search_box = self.driver.find_element(By.XPATH, '/html/body/div[5]/div[1]/div/section/div[1]/div[1]/div/div/div/div[1]/form/input')

        # Check if the element is displayed and enabled
        if search_box.is_displayed() and search_box.is_enabled():
            # Clear the search box and send the address
            search_box.clear()
            search_box.send_keys(self.address)
            
            # Tab over to the search button and return
            i = 0
            tabs = 1
            actions = ActionChains(self.driver)
            for i in range(tabs):
                actions = actions.send_keys(Keys.TAB)
                actions.perform()
            current_element = self.driver.switch_to.active_element
            #highlight(current_element, 3, "blue", 5)
            time.sleep(1)
            current_element.send_keys(Keys.RETURN)
            
        else:
            print("The search box element is not displayed or enabled")

    def scrape_data(self): 
        # Open a new csv in write mode and create a writer object to write to it
        with open('GreatSchools.csv', 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            
            # Wait for the page to be fully loaded
            try:
                wait = WebDriverWait(self.driver, 10)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'li.assigned.unsaved')))
                print('Home page has finished loading')
            except TimeoutError:
                    print('Timed out waiting for page to load')

            # Find all elements with the class 'assigned unsaved'
            elements = self.driver.find_elements(By.CSS_SELECTOR, value ='li.assigned.unsaved')
        
            # Iterate over the elements
            for element in elements:
                # Find the name link element and click it
                name_link = element.find_element(By.CSS_SELECTOR, value ='a.name')
                name_link.click()
                
                # Wait for the first element to load
                try:
                    wait = WebDriverWait(self.driver, 10)
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a')))
                    print('School page has finished loading')
                except TimeoutError:
                        print('Timed out waiting for school page to load')

                # Extract the text from the School District element. NoSuchElementException used to handle missing data
                try:
                    element1 = self.driver.find_element(By.XPATH, '/html/body/div[7]/section[1]/div[1]/div/div/div[1]/div/span[5]/a')
                    text1 = element1.text
                    print('School District: ',text1)
                except NoSuchElementException:
                    text1 = ''
                    print('School District: Blank')
        
                # Extract the text from the School Name element. NoSuchElementException used to handle missing data
                try:
                    element2 = self.driver.find_element(By.CSS_SELECTOR, value ='h1.school-name')
                    text2 = element2.text
                    print('School name: ',text2)
                except NoSuchElementException:
                    text2 = ''
                    print('School name: Blank')
        
                # Extract the number from the School Rating element. NoSuchElementException used to handle missing data
                try:
                    element3 = self.driver.find_element(By.CSS_SELECTOR, value ='.circle-rating--large')
                    # Extract the text from the element
                    text = element3.text
                    number3 = text.split('/')
                    print('School rating: ',number3)
                except NoSuchElementException:
                    number3 = ''
                    print('School rating: Blank')
        
                # Extract the number from the Graduation Rate element, but only if it is a highschool.
                # locate the element containing the grades
                grades_element = self.driver.find_element(By.CSS_SELECTOR, '.school-stats-label')
                
                # extract the text from the element
                grades = grades_element.text
                
                # check if the string "12" is contained in the grades text and if it is a digit
                if '12' in grades and grades.replace('12', '').isdigit():
                  # locate the element containing the graduation rate
                  element4 = self.driver.find_element(By.CSS_SELECTOR, '.percentage')
                
                  # extract the text from the element
                  text4 = element4.text
                  print('Graduation rate: ',text4)
                else:
                  text4 = ''
                  print('Graduation rate: Blank')
                  
                # Extract the number from the Low Income element. NoSuchElementException used to handle missing data
                try:
                  # locate the element containing the low income rate
                  element5 = self.driver.find_element(By.XPATH,'/html/body/div[7]/section[2]/div[1]/div/div[2]/div[10]/div/div[4]/div/div/div[3]/div/div[2]/div/div[1]/div[2]')
                 
                  # extract the text from the element
                  text5 = element5.text
                
                  # split the text on the '%' character and extract the first element
                  number5 = text5.split('%')[0]
                  print('Low income rate: ',number5)
                except NoSuchElementException:
                  # assign a default value to the number5 variable
                  number5 = ''
                  print('Low income rate: Blank')
        
                # Write the extracted text to the CSV file
                #writer.writerow(['District','Name', 'Rating', 'Graduation%', 'Low Income%'])
                writer.writerow([text1, text2, number3, text4, number5])
        
                # Go back to the previous page
                self.driver.back()

    def data_formatting(self):
        pass

    def data_download(self):
        pass

    def close_session(self):
        pass

    def gs_scrape(self):
        self.get_address()
        self.navigate_Greatschools()
        self.enter_address()
        self.scrape_data()
        self.data_formatting()
        self.data_download()
        self.close_session()
        pass

if __name__ == "__main__":
    gs_bot = GreatSchoolsScrape()
    gs_bot.gs_scrape()
    # z_bot = ZillowAPI()
    # z_bot.z_scrape()
