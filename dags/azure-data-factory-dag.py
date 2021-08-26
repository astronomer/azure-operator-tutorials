from airflow import DAG
from airflow.decorators import task
from datetime import datetime, timedelta
from airflow.providers.microsoft.azure.hooks.azure_data_factory import AzureDataFactoryHook

azure_data_factory_conn = 'azure_data_factory_conn'

#Get yesterday's date, in the correct format
yesterday_date = '{{ yesterday_ds_nodash }}'

@task
def run_adf_pipeline(pipeline_name: str, date: str) -> None:
    '''Runs an Azure Data Factory pipeline using the AzureDataFactoryHook and passes in a date parameter'''

    #Create a dictionary with date parameter
    params = {}
    params["date"] = date

    #Make connection to ADF, and run pipeline with parameter
    hook = AzureDataFactoryHook(azure_data_factory_conn)
    hook.run_pipeline(pipeline_name, parameters=params)


with DAG(
    'azure_data_factory',
    start_date=datetime(2019, 1, 1),
    max_active_runs=1,
    schedule_interval=timedelta(minutes=30),
    default_args={
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 0,
    },
    catchup=False
) as dag:

    run_adf_pipeline(pipeline_name="pipeline1", date=yesterday_date)
