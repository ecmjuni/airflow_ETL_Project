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

## Running the Process
You will go to the jupyter notebook ETL_Process.ipynb and set the python kernel 3.12.4 and run sequencially the cells or just "run all".

All dataframes will be separated into 3 CSV sources in the PATH("./Data Layers") representing each layer of the data architecture.

Raw: "./Data Layers/movies_raw.csv"

Silver: "./Data Layers/movies_silver.csv"

Gold: "./Data Layers/movies_gold.csv" - RESULT DATAFRAME