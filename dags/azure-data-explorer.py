"""
### Azure Data Explorer and Airflow

Shows how to call AzureDataExplorer from Airflow using the AzureDataExplorer Operator.

This example assumes you have an ADX account already running and runs a relatively simple query.
"""

from airflow import DAG
from airflow.providers.microsoft.azure.operators.adx import AzureDataExplorerQueryOperator
from datetime import datetime, timedelta

adx_query = '''StormEvents
| sort by StartTime desc
| take 10'''

with DAG(
    'azure_data_explorer',
    start_date=datetime(2020, 12, 1),
    max_active_runs=1,
    schedule_interval='@daily',
    default_args={
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=1)
    },
    catchup=False,
    doc_md=__doc__
) as dag:

    opr_adx_query = AzureDataExplorerQueryOperator(
        task_id='adx_query',
        query=adx_query,
        database='storm_demo',
        azure_data_explorer_conn_id='adx'
    )
