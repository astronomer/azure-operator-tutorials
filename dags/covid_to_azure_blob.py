"""
### Load Covid data to Azure Blob Storage

DAG that uploads data to Azure Blob Storage and sends an email when ran successfully.

This DAG shows how to generate a task for every element in a list and uses the AzureBlobHook to perform the upload.
"""

from airflow import DAG
from airflow.decorators import task
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.email_operator import EmailOperator
from airflow.providers.microsoft.azure.hooks.wasb import WasbHook
from airflow.utils.task_group import TaskGroup
from datetime import datetime, timedelta
import os
import requests


endpoints = ["ca", "co", "ny", "pa", "wa"]
date = "{{ ds_nodash }}"
email_to = ["example@example.com"]


with DAG(
    "covid_data_to_azure_blob",
    start_date=datetime(2020, 12, 1),
    doc_md=__doc__,
    max_active_runs=1,
    schedule_interval="@daily",
    default_args={
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=1),
    },
    catchup=False,  # enable if you don't want historical dag runs to run
) as dag:

    t0 = DummyOperator(task_id="start")

    send_email = EmailOperator(
        task_id="send_email",
        to=email_to,
        subject="Covid to Azure Blob DAG",
        html_content="<p>The Covid to Azure Blob DAG completed successfully. Files can now be found in Azure blob storage. <p>",
    )

    with TaskGroup("covid_task_group") as covid_group:
        for endpoint in endpoints:

            @task(task_id="generate_file_{0}".format(endpoint))
            def upload_to_azure_blob(endpoint: str, date: str) -> None:
                # Instanstiate
                azurehook = WasbHook(wasb_conn_id="azure_blob")

                # Make request to get Covid data from API
                url = "https://covidtracking.com/api/v1/states/"
                filename = "{0}/{1}.csv".format(endpoint, date)
                res = requests.get(url + filename)

                # Take string, upload to S3 using predefined method
                azurehook.load_string(string_data=res.text, container_name="covid-data", blob_name=filename)

            upload_to_azure_blob(endpoint=endpoint, date=date)

    t0 >> covid_group >> send_email
