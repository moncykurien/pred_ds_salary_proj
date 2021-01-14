from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd
from apps.core.logger import Logger

class GlassDoorScrapper:

    def __init__(self, run_id, data_path, mode, chrome_driver_path, sleep_time):
        self.run_id = run_id
        self.data_path = data_path
        #self.logger = Logger(self.run_id, 'GlassDoorScrapper', mode)

        # Initializing the webdriver
        options = webdriver.ChromeOptions()
        # Uncomment the line below if you'd like to scrape without a new Chrome window every time.
        # options.add_argument('headless')

        # Change the path to where chromedriver is in your home folder.
        self.driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)
        self.driver.set_window_size(1120, 1000)
        self.sleep = sleep_time

    def get_jobs(self, num_jobs, verbose, keyword = 'data science'):
        '''Gathers jobs as a dataframe, scraped from Glassdoor'''
        self.url = 'https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword='+keyword+'&sc.keyword='+keyword+'&locT=&locId=&jobType='
        print(self.url)
        self.driver.get(self.url)
        jobs = []

        while len(jobs) < num_jobs:  # If true, should be still looking for new jobs.
            # Let the page load. Change this number based on your internet speed.
            # Or, wait until the webpage is loaded, instead of hardcoding it.
            time.sleep(self.sleep)

            # Test for the "Sign Up" prompt and get rid of it.
            try:
                self.driver.find_element_by_class_name("selected").click()
            except ElementClickInterceptedException:
                pass

            time.sleep(.1)

            try:
                self.driver.find_element_by_xpath('//*[@class="SVGInline modal_closeIcon"]').click()
            except NoSuchElementException:
                pass

            # Going through each job in this page

            job_buttons = self.driver.find_elements_by_xpath("//*[@class='jlGrid hover p-0 ']/li")
            # Job Listing. These are the buttons we're going to click.
            print(job_buttons)
            for job_button in job_buttons:
                print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
                if len(jobs) >= num_jobs:
                    break

                try:
                    job_button.click()  # You might
                except Exception as e:
                    print(e)
                time.sleep(1)
                collected_successfully = False

                while not collected_successfully:
                    try:
                        xpath = '*//div[@class="empWrapper ctasTest"]/div/div'
                        company_name = self.driver.find_element_by_xpath(xpath+'[1]').text
                        location = self.driver.find_element_by_xpath(xpath+'[3]').text
                        job_title = self.driver.find_element_by_xpath(xpath+'[2]').text
                        job_description = self.driver.find_element_by_xpath('*//div[@class="jobDescriptionContent desc"]').text
                        collected_successfully = True
                    except:
                        time.sleep(5)

                try:
                    salary_estimate = self.driver.find_element_by_xpath(xpath+'[4]/span').text
                except NoSuchElementException:
                    salary_estimate = -1  # You need to set a "not found value. It's important."

                try:
                    rating = self.driver.find_element_by_xpath(xpath+'[1]/span').text
                except NoSuchElementException:
                    rating = -1  # You need to set a "not found value. It's important."

                # Printing for debugging
                if verbose:
                    print("Job Title: {}".format(job_title))
                    print("Salary Estimate: {}".format(salary_estimate))
                    print("Job Description: {}".format(job_description[:500]))
                    print("Rating: {}".format(rating))
                    print("Company Name: {}".format(company_name))
                    print("Location: {}".format(location))

                # Going to the Company tab...
                # clicking on this:
                # <div class="tab" data-tab-type="overview"><span>Company</span></div>
                try:
                    self.driver.find_element_by_xpath('*//div[@class="tab" and @data-tab-type="overview"]').click()

                    try:
                        # <div class="infoEntity">
                        #    <label>Headquarters</label>
                        #    <span class="value">San Francisco, CA</span>
                        # </div>
                        headquarters = self.driver.find_element_by_xpath('*//div[@class="infoEntity"]//label[text()="Headquarters"]//following-sibling::*').text
                    except NoSuchElementException:
                        headquarters = -1

                    try:
                        size = self.driver.find_element_by_xpath('*//div[@class="infoEntity"]//label[text()="Size"]//following-sibling::*').text
                    except NoSuchElementException:
                        size = -1

                    try:
                        founded = self.driver.find_element_by_xpath('*//div[@class="infoEntity"]//label[text()="Founded"]//following-sibling::*').text
                    except NoSuchElementException:
                        founded = -1

                    try:
                        type_of_ownership = self.driver.find_element_by_xpath(
                            './/div[@class="infoEntity"]//label[text()="Type"]//following-sibling::*').text
                    except NoSuchElementException:
                        type_of_ownership = -1

                    try:
                        industry = self.driver.find_element_by_xpath(
                            './/div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*').text
                    except NoSuchElementException:
                        industry = -1

                    try:
                        sector = self.driver.find_element_by_xpath(
                            './/div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*').text
                    except NoSuchElementException:
                        sector = -1

                    try:
                        revenue = self.driver.find_element_by_xpath(
                            './/div[@class="infoEntity"]//label[text()="Revenue"]//following-sibling::*').text
                    except NoSuchElementException:
                        revenue = -1

                    try:
                        competitors = self.driver.find_element_by_xpath(
                            './/div[@class="infoEntity"]//label[text()="Competitors"]//following-sibling::*').text
                    except NoSuchElementException:
                        competitors = -1

                except NoSuchElementException:  # Rarely, some job postings do not have the "Company" tab.
                    headquarters = -1
                    size = -1
                    founded = -1
                    type_of_ownership = -1
                    industry = -1
                    sector = -1
                    revenue = -1
                    competitors = -1

                if verbose:
                    print("Headquarters: {}".format(headquarters))
                    print("Size: {}".format(size))
                    print("Founded: {}".format(founded))
                    print("Type of Ownership: {}".format(type_of_ownership))
                    print("Industry: {}".format(industry))
                    print("Sector: {}".format(sector))
                    print("Revenue: {}".format(revenue))
                    print("Competitors: {}".format(competitors))
                    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

                jobs.append({"Job Title": job_title,
                             "Salary Estimate": salary_estimate,
                             "Job Description": job_description,
                             "Rating": rating,
                             "Company Name": company_name,
                             "Location": location,
                             "Headquarters": headquarters,
                             "Size": size,
                             "Founded": founded,
                             "Type of ownership": type_of_ownership,
                             "Industry": industry,
                             "Sector": sector,
                             "Revenue": revenue,
                             "Competitors": competitors})
                # add job to jobs

            # Clicking on the "next page" button
            try:
                self.driver.find_element_by_xpath('.//li[@class="next"]//a').click()
            except NoSuchElementException:
                print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs,
                                                                                                             len(jobs)))
                break

        return pd.DataFrame(jobs)  # This line converts the dictionary object into a pandas DataFrame.