from apps.scrapper.scrapper import GlassDoorScrapper
import pandas as pd
from apps.core.logger import Logger

class ScrapeLoadValidate:
    def __init__(self, run_id, data_path):
        self.run_id = run_id
        self.data_path = data_path
        self.driver = './apps/driver/chromedriver'
        #self.logger = Logger(self.run_id,'ScrapeLoadValidate', 'training')

    def get_data_glassdoor(self, job_title = 'data scientist'):
        print('In scrapLoadValidate')
        glassdoor_scrapper = GlassDoorScrapper(self.run_id,self.data_path, 'training', self.driver,5)
        df = glassdoor_scrapper.get_jobs(1000,False,job_title)
        print(df)
        df.to_csv('./apps/'+self.data_path+'/raw_training_data.csv', index=False, sep=',',line_terminator='\r\n')
        return df
