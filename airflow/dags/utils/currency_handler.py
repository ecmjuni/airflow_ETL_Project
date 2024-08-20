import requests
import re

def extract_currency_symbol(currency_string):
    pattern = r'[$€£]'
    
    match = re.search(pattern, currency_string)
    
    if match:
        return match.group()
    else:
        return None

def convert_currency_string_to_int(currency_string):
    cleaned_string = re.sub(r'[^\d\.\smillionbilliontrillion]', '', currency_string.lower()).strip()
    
    multiplier = 1
    if 'million' in cleaned_string:
        multiplier = 10**6
    elif 'billion' in cleaned_string:
        multiplier = 10**9
    elif 'trillion' in cleaned_string:
        multiplier = 10**12
    
    number_part = re.findall(r'\d+\.\d+|\d+', cleaned_string)
    if number_part:
        number = float(number_part[0])
    else:
        number = 0

    return int(number * multiplier)

def convert_symbols(symbol):

    if(symbol == '$'):
        return "USD"
    if(symbol == '€'):
        return "EUR"
    if(symbol == '£'):
        return "GBP"
    
    return ""

def dolar_converter(value):

    if value != '0':
        currency, value_str = value.split(" ")
        number_value = float(value_str.replace(',', '.'))

        currency_supported = ['GBP', 'EUR', 'USD']
        if currency not in currency_supported:
            return 0
        
        url = f"https://api.exchangerate-api.com/v4/latest/{currency}"
        response = requests.get(url)
        data = response.json()
        rate_conv = data['rates']['USD']

        dolar_value = number_value * rate_conv

        return dolar_value
    else: 
        return 0.0

def range_money_filter(value):
    if(value > 10000000 and value < 20000000):
        return 0
    else: 
        return value
    
def range_money_outlier(value):
    if(value < 65000 or value > 500000000):
        return True
    else: 
        return False