# Greatschools Web Scraper

This project is a web scraper that retrieves information about schools from the Great Schools website and stores it in a CSV file. The user is prompted to enter an address, and the scraper navigates to the Great Schools website, enters the address into a search box, and submits the search. The scraper then retrieves information about the schools in the search results and stores it in the CSV file.

## Requirements:
- Python 3.7 or higher
- Selenium
- Chromedriver
## Usage
### Clone the repository:
- git clone https://github.com/Xman94/GreatSchoolsScrape
### Navigate to the project directory:
- cd GreatSchoolsScrape
### Run the script:
- on line 27 change the chrome driver path to where you installed it on your local machine
- python great_schools_scrape.py
- Follow the prompts to enter an address. The scraper will retrieve information about the schools in the search results and store it in a CSV file named "GreatSchools.csv" in the project directory.
## Notes
- The script uses ChromeDriver to control the Chrome browser, so you will need to have Chrome installed on your machine.
- The script may take a few minutes to run, depending on the number of schools in the search results.
- The script may not work if the Great Schools website changes its layout or the elements used on the website change.
- The script may not work if the Chrome browser or ChromeDriver are updated, as the script relies on their current functionality.
