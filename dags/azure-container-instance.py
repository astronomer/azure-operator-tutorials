from airflow import DAG
from airflow.providers.microsoft.azure.operators.azure_container_instances import AzureContainerInstancesOperator
from datetime import datetime, timedelta

with DAG(
    'azure_container_instances',
    start_date=datetime(2020, 12, 1),
    max_active_runs=1,
    schedule_interval='@daily',
    default_args={
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=1)
    },
    catchup=False
) as dag:

    opr_run_container = AzureContainerInstancesOperator(
        task_id='run_container',
        ci_conn_id='azure_container_conn_id',
        registry_conn_id=None,
        resource_group='adf-tutorial',
        name='astrotutorial',
        image='hello-world:latest',
        region='East US',
        fail_if_exists=False

    )
