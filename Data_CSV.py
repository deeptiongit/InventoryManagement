import json
import os
import pandas as pd

Shipping_data = "/app/backend/prediction_service/phi3/src/DataCurating/pseudo_summaries/shippingOrders_jsons"


Shipping_orders_csv = pd.DataFrame()
Purchase_orders_csv = pd.DataFrame()
Invoice_csv = pd.DataFrame()

for file in os.listdir(Shipping_data):
    with open (os.path.join(Shipping_data, file) , 'r') as f:
        data = json.load(f)
        df = pd.json_normalize(data)
        Shipping_orders_csv = pd.concat([Shipping_orders_csv, df], ignore_index=True)


Shipping_orders_csv.to_csv("/app/backend/prediction_service/phi3/src/DataCurating/CSV_Files/Shipping_Orders.csv" , index = False)
