## Information about the libraries
All functions created to treat the data during the Transformations are into ./utils folder.
The main process of ETL was based into an object called "movies_etl_process" that was written into the ETL_Process.ipynb in cell 3.

## RAW Layer
First Appoach was to extract the data from the API endpoint using web scraping module "request" and so create the RAW Layer to our datalake considering CSV format and a initial schema.

        {
            "film": object, 
            "year": object,
            "wikipedia_url": object, 
            "Oscar winner": object, 
            "original budget": float, 
            "budget converted to USD": float
        }

## Silver Layer
To treat the budget data we used the "./utils/currency_handler.py" library. After treat the budget string data using regular expressions with the "re" module for extracting the integer values and currencies from the Budget column we created 2 new columns "budget_original_currency" and "budget_original_value" as a way to avoid creation of outliers by transformation phase.

For conversion the currencies was consumed data from the API endpoint "https://api.exchangerate-api.com/v4/latest/{currency}" that provided to us the conversion rates to USD.

Schema:
        {
            "film": object
            "year": object
            "wikipedia_url": object
            "Oscar winner": bool
            "original budget": object
            "budget converted to USD": float64
            "budget_original_currency": object
            "budget_original_value": int64
            "outlier": bool
        }

After It was created a column to flag possible outliers considering 0 values and value < 65000 or value > 500000000.

## Gold Layer - RESULT DATAFRAME
In this phase of the process was added the filtering for the values of Budget in range of ($10000000 - $20000000) and the treatment of date values to int using regular expression provided by "./utils/date_handler".

Final Schema:
        {
            "film": object
            "year": object
            "wikipedia_url": object
            "Oscar winner": bool
            "original budget": object
            "budget_original_currency": object
            "budget_original_value": int64
            "budget converted to USD": float64
            "outlier": bool
        }

