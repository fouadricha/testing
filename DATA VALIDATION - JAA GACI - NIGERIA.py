# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 10:20:43 2022

@author: Fouad.Youssef
"""

path= r"C:\Users\Fouad.Youssef.JAG\Desktop\Spyder\JAA GACI\Cost expectation by order JAA.xlsx"

import pandas as pd
import numpy as np
df = pd.read_excel(path)

"""
JAA - NIGERIA
"""


"""
FILTERING BASED ON ITEM CODES / COUNTRY / SHIPMENT STATUS #TO NOT CONSIDER IT
"""
df = df.loc[(df['ShipmentStatus'] != 'received' ) & (df['ShipmentStatus'] != "Received") & (df['ShipmentStatus'] != "Recieved") & (df['ShipmentStatus'] != "Receieved" )]
df = df.loc[(df['ItemType'] == "TECHNICAL") | (df['ItemType'] == "SURFACTANT") | (df['ItemType'] == "Agrochemical")]
remove_items_useless = df[
                            (df['ItemCode'] == "20ft") 
                          | (df['ItemCode'] == "40ft") 
                          | (df['ItemCode'] == "40HC") 
                          | (df['ItemCode'] == "40HQ") 
                          | (df['ItemCode'] == "20FT") 
                          | (df['ItemCode'] == "40hq")
                          | (df['ItemCode'] == "LCL")                                
                          | (df['ItemCode'] == "othercharges")
                          | (df['ItemCode'] == "SONCAP") 
                          | (df['ItemCode'] == "C-Charge")
                          | (df['ItemCode'] == "N-013") #Transportation LSP
                          | (df['ItemCode'] == "Cylinder")
                          | (df['ItemCode'] == "FR-001")
                          | (df['ItemCode'] == "FR-002")
                          | (df['ItemCode'] == "FR-20")
                          | (df['ItemCode'] == "FR-40")
                                                             ].index
df.drop(remove_items_useless, inplace= True)

"""
MISSING BASIC DATA ENTRY AND CONDITIONS
"""
df_missing_data = df.loc[
                (df['CommodityType'].isnull() == True) 
            |   (df['Incoterm'].isnull() == True) 
            |   (df['SHippingLine'].isnull() == True) 
            |   (df['Port of loading'].isnull() == True) 
            |   (df['Port of discharge/TO'].isnull() == True)
            |   (df['CTNSIZE'].isnull() == True)
            |   (df['CTNQty'].isnull() == True)
            |   (df['orderQuantity'].isnull() == True)
            |   (((df['Freight'].isnull() == True ) | (df['Freight'] == 0)) & ((df['Incoterm'] == "FOB") | (df['Incoterm'] == "EXW")))
            |   (((df['Transportation'].isnull() == True) | (df['Transportation'] == 0)) & (df['customeraux'] == 152))
            |   ((df['Clearing'].isnull()== True ) | (df['Clearing'] == 0 ))
              ]
filtered_missing_data = df_missing_data[['User2' , 'PO#' , 'SD#' ,'ItemCode','ItemType']].drop_duplicates() #THE COLUMNS WE NEED TO SHOW


"""
STATUS DISCREPANCIES IN DATA ENTRY
"""
df_status_true = df.loc[   ((df['OrderStatus'] == "Shipped") & (df['ShipmentStatus'] == "Shipped")) 
                         | ((df['OrderStatus'] == "Shipped") & (df['ShipmentStatus'] == "At Port")) 
                         | ((df['OrderStatus'] == "unShipped") & (df['ShipmentStatus'] == "order")) 
                         ]
df_status_discrepancies = pd.concat([df, df_status_true]).drop_duplicates(keep=False) #this method drops the duplicates using "FALSE" statement it removes every duplicate ( In other words, the main DF minus the correct status DF)
filtered_status = df_status_discrepancies[['User2' , 'PO#' , 'SD#', 'OrderStatus' , 'ShipmentStatus']].drop_duplicates() #THE COLUMNS WE NEED TO SHOW



print(filtered_missing_data)
print(filtered_status)


"""
EXTRACT THE DATA TO EXCEL
"""
with pd.ExcelWriter('DATA DISCREPANCY - JAA - Nigeria.xlsx') as writer:
 filtered_missing_data.to_excel(writer, sheet_name='MISSING DATA', index=False)
 filtered_status.to_excel(writer, sheet_name='SHIPPED-UNSH DISCREPANCIES', index=False)
