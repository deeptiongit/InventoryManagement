import json
import os
import pandas as pd

Shipping_data = "/path/to/ShippingOrdersdatajsons"
Purchase_data = "/path/to/PurchaseOrdersdatajsons"
Invoice_data = "/path/to/Invoicedatajsons"


Shipping_orders_csv = pd.DataFrame()
Purchase_orders_csv = pd.DataFrame()
Invoice_csv = pd.DataFrame()

for file in os.listdir(Shipping_data):
    with open (os.path.join(Shipping_data, file) , 'r') as f:
        data = json.load(f)
        df = pd.json_normalize(data)
        Shipping_orders_csv = pd.concat([Shipping_orders_csv, df], ignore_index=True)


for file in os.listdir(Purchase_data):
    with open (os.path.join(Purchase_data, file) , 'r') as f:
        data = json.load(f)
        df = pd.json_normalize(data)
        Purchase_orders_csv = pd.concat([Purchase_orders_csv, df], ignore_index=True)

for file in os.listdir(Invoice_data):
    with open (os.path.join(Invoice_data, file) , 'r') as f:
        data = json.load(f)
        df = pd.json_normalize(data)
        Invoice_csv = pd.concat([Invoice_csv, df], ignore_index=True)

Shipping_orders_csv.to_csv("/path/to/DataCurating/CSV_Files/Shipping_Orders.csv" , index = False)
Purchase_orders_csv.to_csv("/path/to/DataCurating/CSV_Files/Purchase_Orders.csv" , index = False)
Invoice_csv.to_csv("/path/to/DataCurating/CSV_Files/Invoices.csv" , index = False)
