from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import csv
import time
import re

class GreatSchoolsScrape:
    def __init__(self):
        """
        This code is setting up the Chrome web browser for use in the script. 
        The ChromeService object is created with the path to the ChromeDriver 
        executable, which is a separate program that allows the script to interact 
        with the Chrome browser. The ChromeOptions object is created and the 
        "no-sandbox" flag is added as an argument. This flag tells the Chrome 
        browser to run without the sandbox security feature enabled. The Chrome 
        browser is then started with the "no-sandbox" flag and the ChromeService 
        object, and the window is maximized.
        """
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
        """ 
        this defines a function called 'get address', a while loop is being used 
        to prompt the user to enter an address. The loop will continue until the 
        user enters a non-empty string for the address. When the loop starts, 
        the value of the self.address variable is an empty string. The value of 
        self.address is checked at the beginning of each iteration of the loop. 
        If it is still an empty string, the user is prompted to enter an address. 
        Once the user enters a non-empty string, the value of self.address is 
        updated and the loop ends.
        """
        self.address = ""
        while self.address == "":
            self.address = input('Please Enter an Address: ')

    def navigate_Greatschools(self):
        """ 
        This code is defining a function called navigate_Greatschools in the 
        GreatSchoolsScrape class. The function uses the get method of the 
        self.driver object to navigate to the Great Schools website. The 
        WebDriverWait function is called with a 10 second timeout to wait for 
        the website to load before continuing with the script.
        """
        self.driver.get('https://www.greatschools.org/')
        print('Navigating to Great Schools')
        WebDriverWait(self.driver, 10)

    def enter_address(self):
        """ This code is defining a function called enter_address that is used 
        to enter an address into a search box on a webpage and submit it. The 
        function first uses the find_element method of the self.driver object 
        to locate the search box element on the webpage using its XPath. Then, 
        it checks if the element is displayed and enabled. If it is, the 
        function clears the search box, enters the value of the self.address 
        attribute into the search box, and then simulates the press of the "Tab" 
        key and the "Return" key to submit the search. If the element is not 
        displayed or enabled, the function prints a message indicating this.
        """
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
        """ 
        This is a method that scrapes data from the Great Schools website. 
        It first opens a new CSV file in write mode and creates a writer object 
        to write to it. Then, it waits for the home page to be fully loaded and 
        finds all elements that match the CSS selector 'li.assigned.unsaved'. 
        
        It then iterates over these elements and for each element, it finds the 
        name link element and gets the 'href' attribute value of the link. 
        
        It then navigates to the URL of the link and waits for the school page 
        to be fully loaded. After the school page has loaded, it attempts to 
        extract the text from several elements on the page: the School District 
        element, the School Name element, and the School Rating element.
        If any of these elements are not found, it handles the exception by 
        setting the text value to an empty string. 
        
        It then checks if the school 
        is a high school by checking if the string '12' is in the grades element 
        text and if the grades element text can be converted to an integer. 
        If the school is a high school, it attempts to extract the text from 
        the Graduation Rate element. If it is not a high school or if the 
        Graduation Rate element is not found, it sets the graduation rate to 
        an empty string.
        
        Finally, it writes the extracted text and numbers to 
        the CSV file and closes the file."""
        
        #open a new csv and create a writer object to write to it
        with open('GreatSchools.csv', 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            
            #Wait for the page to be fully loaded         
            try:
                wait = WebDriverWait(self.driver, 10)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'li.assigned.unsaved')))
                print('Home page has finished loading')
            except TimeoutError:
                    print('Timed out waiting for page to load')
            
            elements = self.driver.find_elements(By.CSS_SELECTOR, 'li.assigned.unsaved')
            
            # Initialize an empty list to store the href links
            href_links = []
            
            # Iterate over the elements
            for element in elements:
                # Find the name link element
                name_link = element.find_element(By.CSS_SELECTOR, 'a.name')
            
                # Get the href value of the link
                href = name_link.get_attribute('href')
            
                # Append the href value to the list
                href_links.append(href)

            # Iterate through the links
            for link in href_links:
                time.sleep(5)
           
                # Navigate to the URL
                self.driver.get(link)
                
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
                # Find all elements that match the CSS selector
                    element3 = self.driver.find_element(By.CSS_SELECTOR, value ='.circle-rating--large')
                    number3 = element3.text
                    print('School rating:', number3)
                except NoSuchElementException:
                    number3 = ''
                    print('School rating: Blank')
                    
                # Extract the number from the Graduation Rate element, but only if it is a highschool.
                # locate the element containing the grades
                grades_element = self.driver.find_element (By.XPATH, '/html/body/div[7]/section[1]/div[2]/div/div/div/div[3]/span')
                
                # extract the text from the element
                grades = grades_element.text
                
                # check if the string "12" is contained in the grades text and if it is a digit
                if '12' in grades:
                  # locate the element containing the graduation rate
                  element4 = self.driver.find_element(By.XPATH, '/html/body/div[7]/section[2]/div[1]/div/div[2]/div[4]/div/div[4]/div/div/div/div[1]/div[2]/div[1]')
                
                  # extract the text from the element
                  text4 = element4.text
                  print('Graduation rate: ',text4)
                else:
                  text4 = ''
                  print('Graduation rate: Blank')
                try:
                    # Locate the element containing the low income rate
                    element5 = self.driver.find_element(By.CSS_SELECTOR, value = '.label-subtext')
                    # Extract the text from the element
                    text5 = element5.text
                    # Use a regular expression to extract the number
                    match = re.search(r'(\d+)', text5)
                    if match:
                        # Extract the number from the match object
                        number5 = match.group(1)
                        print('Low income rate:', number5)
                    else:
                        number5 = ''
                        print('Low income rate: Blank')
                except NoSuchElementException:
                    # Assign a default value to the number5 variable
                    number5 = ''
                    print('Low income rate: Blank')
        
                # Write the extracted text to the CSV file
                writer.writerow([text1, text2, number3, text4, number5])
                print('driver.back check')

    def close_session(self):
        self.driver.close()

    def gs_scrape(self):
        self.get_address()
        self.navigate_Greatschools()
        self.enter_address()
        self.scrape_data()
        self.close_session()

if __name__ == "__main__":
    gs_bot = GreatSchoolsScrape()
    gs_bot.gs_scrape()