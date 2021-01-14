from apps.data_ingestion.scrap_load_validate import ScrapeLoadValidate
from apps.core.config import Config

if __name__ == '__main__':
    try:
        #initiate the Config class
        config = Config()
        #get run_id
        run_id = config.get_run_id()
        #Get training data file path
        data_path = config.training_data_path
        #initiate TrainModel object
        scrap_load_validate = ScrapeLoadValidate(run_id,data_path)
        df = scrap_load_validate.get_data_glassdoor()
        print(df.head())
    except Exception as e:
        print(e)