# How to run the ETL Process

## Depencies installation
For running the ETL you'll need to install the VisualStudio Code provided by Microsoft:
https://code.visualstudio.com/Download

After this will need to install Python 3.12.4 under the link below:
https://www.python.org/downloads/release/python-3124/
Verify the version of you OS before the installation.

After installing Python 3.12.4 you will execute visual studio code.

Search in Extension tab of Visual Studio Code by Jupyter extension and install it.

Open a terminal and go to the project folder.

Run the command below to install all depencies to run the ETL process properly:

```
pip install -r requirement.txt
```

## Create Docker Image
Execute the commands bellow to create the docker image.

```
docker build --pull --rm -f "DockerFile" -t airflow-etl "." 
```

## Build the Continer to run the Airflow

Execute the commands bellow to build the docker image into the container instance.

```
docker compose -f "docker-compose.yml" up -d --build 
```

## Run ETL pipeline

Go to URL: "localhost:8080/home"

Trigger the DAG and follow the pipeline data flow.

Raw: "./Data Layers/movies_raw.csv"

Silver: "./Data Layers/movies_silver.csv"

Gold: "./Data Layers/movies_gold.csv" - RESULT DATAFRAME