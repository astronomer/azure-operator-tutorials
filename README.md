# azure-operator-tutorials
This repo contains an Astronomer project with multiple example DAGs showing how to use Azure service operators in Airflow.

## DAG Overview
This repo contains DAGs to interact with the following Azure services. Links will direct you to a detailed guide walking through how to use the operators.

 - [Azure Container Instances](https://www.astronomer.io/guides/airflow-azure-container-instances)
 - [Azure Data Explorer](https://www.astronomer.io/guides/airflow-azure-data-explorer)


## Getting Started
The easiest way to run these example DAGs is to use the Astronomer CLI to get an Airflow instance up and running locally:

 1. [Install the Astronomer CLI](https://www.astronomer.io/docs/cloud/stable/develop/cli-quickstart)
 2. Clone this repo somewhere locally and navigate to it in your terminal
 3. Initialize an Astronomer project by running `astro dev init`
 4. Start Airflow locally by running `astro dev start`
 5. Navigate to localhost:8080 in your browser and you should see the tutorial DAGs there
