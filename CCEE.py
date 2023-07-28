

URL = "https://www.ccee.org.br/documents/80415/919444"
RESOURCEID = "01bdd7c7-9a3a-5c46-ef6b-bcb8c48e7daa"
STORE_DATA = "downloadedData"
FILE_NAME = "InfoMercado_Dados_Individuais-Dez2022"

import requests
import os
import csv
import json
import pandas as pd
from datetime import datetime

def getCCEEData():
        
        # Contact API
        try:
            request = f"{URL}/{FILE_NAME}.xlsx/{RESOURCEID}"
            print(f"Envio requisição '{request}': {datetime.now()}")
            response = requests.get(request)
            response.raise_for_status()
            print(f"Resposta obtida: {datetime.now()}")
        except requests.RequestException:
            return None
        
        # Parse response
        try:
            file = f"{STORE_DATA}/{FILE_NAME}.xlsx"
            print(f"Inicio da gravação do arquivo '{file}' : {datetime.now()}")
            with open(file, 'wb') as f:
                f.write(response.content)
            
            del(response)
            
            print(f"Fim da gravação do arquivo '{file}' : {datetime.now()}")
            
            print(f"Inicio da abertura do arquivo '{file}' : {datetime.now()}")
            df = pd.read_excel(file, sheet_name="003 Consumo")
            print(f"Fim da abertura do arquivo '{file}' : {datetime.now()}")
            # get keys
            keys = df.iloc[15, 1:].values

            # get values
            values = df.iloc[16:348702, 1:].values

            del(df)
            
            data = []
            for value in values:
                dict = {}
                for i, key in enumerate(keys):
                    dict[key] = value[i]
                    data.append(dict)

            del(keys)
            del(values)
            
            return data
        
        except (KeyError, TypeError, ValueError):
            return None
        
def storeCCEEData(data):
    
    csv_filename = f'{STORE_DATA}/{FILE_NAME}.csv'
    
    with open(csv_filename, 'w', newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile,delimiter=';')
        writer.writerow(data[0].keys())

        # Write data in CSV file
        for item in data:
            writer.writerow(item.values())
        
    ## Save data to JSON
    #json_filename = f'{STORE_DATA}/{FILE_NAME}.json'
    #with open(json_filename, 'w', encoding="utf-8") as jsonfile:
    #    json.dump(data, jsonfile)
            
    return True

def readCCEEStoredData():
    
    csv_filename = f'{STORE_DATA}/{FILE_NAME}.csv'
    
    if not (os.path.isfile(csv_filename)):
        return None
    
    return pd.read_csv(csv_filename, delimiter=";",encoding="utf-8")