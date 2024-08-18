import pandas as pd
import requests as rq

import utils.currency_handler as currency_handler
import utils.date_handler as date_handler

class movies_etl_process():

    def __init__(self):
        self.url_api = "http://oscars.yipitdata.com/"
        # Raw data layer's Schema
        self.main_schema = {
            "film": pd.Series(dtype='str'), 
            "year": pd.Series(dtype='str'),
            "wikipedia_url": pd.Series(dtype='str'), 
            "Oscar winner": pd.Series(dtype='str'), 
            "original budget": pd.Series(dtype='float'), 
            "budget converted to USD": pd.Series(dtype='float')
        }

        self.movie_df = pd.DataFrame(self.main_schema)

    def movie_web_scraping(self):
        res_api = rq.get(self.url_api)

        if res_api.status_code == 200:
            res_json = res_api.json()
            
            for results in res_json['results']:
                if len(results["films"]) > 0:
                    row_temp = []
                    for film in results["films"]:

                        details_json = rq.get(film["Detail URL"])
                        if details_json.status_code == 200:
                            details_json.encoding = 'utf-8'
                            details_json = details_json.json()
                            budget_temp = details_json.get("Budget") if not None else 0
                        else:
                            budget_temp = 0.0

                        temp = {
                            "film": film["Film"], 
                            "year": "",
                            "wikipedia_url": film["Wiki URL"], 
                            "Oscar winner": film["Winner"], 
                            "original budget": budget_temp,
                            "budget converted to USD": 0.0
                        }
                        row_temp.append(temp)

                    movie_temp = pd.DataFrame(row_temp)
                    movie_temp["year"] = results["year"]

                    self.movie_df = pd.concat([self.movie_df, movie_temp])
    
            self.movie_df.to_csv("/opt/airflow/data_layers/movies_raw.csv", sep=';', index=None)
        else:
            print("The API URL is unavailable")


    def cleanning_dataframe(self):
        self.movie_df = pd.read_csv("/opt/airflow/data_layers/movies_raw.csv", sep=";")

        # Currency treatment
        self.movie_df["original budget"] = self.movie_df["original budget"].astype(str)

        self.movie_df["budget_original_currency"] = self.movie_df["original budget"].apply(currency_handler.extract_currency_symbol)
        self.movie_df["budget_original_currency"] = self.movie_df["budget_original_currency"].fillna(" ")
        self.movie_df["budget_original_currency"] = self.movie_df["budget_original_currency"].apply(currency_handler.convert_symbols)
        
        self.movie_df["budget_original_value"] = self.movie_df["original budget"].apply(currency_handler.convert_currency_string_to_int)

        self.movie_df["original budget"] = self.movie_df["budget_original_currency"].astype(str) + " " +  self.movie_df["budget_original_value"].astype(str)

        self.movie_df["budget converted to USD"] = self.movie_df["original budget"].apply(currency_handler.dolar_converter)

        # Budget outlier treatment
        self.movie_df["outlier"] = self.movie_df["budget converted to USD"].apply(currency_handler.range_money_outlier)

        self.movie_df.to_csv("/opt/airflow/data_layers/movies_silver.csv", sep=';', index=None)

    def filtering_to_gold(self):
        self.movie_df = pd.read_csv("/opt/airflow/data_layers/movies_silver.csv", sep=";")

        self.movie_df["budget converted to USD"] = self.movie_df["budget converted to USD"].apply(currency_handler.range_money_filter)

        self.movie_df["year"] = self.movie_df["year"].apply(date_handler.extract_year)

        self.movie_df = self.movie_df[["film",
                                       "year",
                                       "wikipedia_url",
                                       "Oscar winner",
                                       "original budget",
                                       "budget_original_currency",
                                       "budget_original_value",
                                       "budget converted to USD",
                                       "outlier"]]

        self.movie_df.to_csv("/opt/airflow/data_layers/movies_gold.csv", sep=';', index=None)