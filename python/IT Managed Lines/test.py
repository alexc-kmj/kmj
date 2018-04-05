#########################################################
#Alex Carder, July 2016                                 #
#Update ListPrice in HP for the price on Amazon         #
#Modified 9/14/16, Split SKU into PLC & PartNumber      #
#########################################################

import pyodbc
import csv
import time

def open_odbc_connection(DSN,UID,PWD):
    return pyodbc.connect('DSN='+DSN+';UID='+UID+';PWD='+PWD+';')
    
def run_sixbit_sql_statement(ODBC_CONN, SQL):
    #set cursor for connection
    CUR_OBJ = ODBC_CONN.cursor()
    print ('cursor created')
    #execute SQL statement
    CUR_OBJ.execute(SQL)
    print ('update ran')

    result = []
    result = [dict(ListingID=row[0], SKU=row[1], InventoryID=row[2], QtyUncommitted=row[3], QtyRemaining=row[4]) for row in CUR_OBJ.fetchall()]

    return result

def run_hp_sql_statement(ODBC_CONN, SQL):
    #set cursor for connection
    CUR_OBJ = ODBC_CONN.cursor()
    #print ('cursor created')
    #execute SQL statement
    CUR_OBJ.execute(SQL)
    #print ('update ran')

    result = [dict(SKU=row[0], Quantity=row[1]) for row in CUR_OBJ.fetchall()]

    return result

# Change the stuff below this text
CSV_TO_READ_DEL = '\t'   # The delimiter on the CSV you are reading
HP_ODBC_CONN_NAME = 'HPCommerce'         # The ODBC connection name
HP_ODBC_USER = ''                        # The ODBC user name, '' if there is no user required
HP_ODBC_PASS = ''                        # The ODBC pass, '' if there is no password required
# Change the stuff above this text

# SQL SERVER #
SIXBIT_ODBC_CONN_NAME = 'SixBit'                   # The ODBC connection name
SIXBIT_ODBC_USER = 'sa_sb'                         # The ODBC user name, '' if there is no user required
SIXBIT_ODBC_PASS = 'S1xb1tR0x'                     # The ODBC pass, '' if there is no password required
# SQL SERVER #

#Open Database Connection
HP_ODBC_CONN = open_odbc_connection(HP_ODBC_CONN_NAME, HP_ODBC_USER, HP_ODBC_PASS)

SIXBIT_ODBC_CONN = open_odbc_connection(SIXBIT_ODBC_CONN_NAME, SIXBIT_ODBC_USER, SIXBIT_ODBC_PASS)

HP_SQL = "SELECT FLOOR(IFNULL(p.OnHand, 0) - IFNULL(coo.CommittedOnOrders, 0)) FROM Plc plc \
        INNER JOIN Imaster p ON plc.PLCID = p.PLCID LEFT JOIN ( SELECT oi.PartID, SUM(oi.Shipped) AS CommittedOnOrders FROM SalesOrder so INNER JOIN [Order] o on so.OrderNumber = o.OrderNumber \
        INNER JOIN OrderItem oi ON o.OrderNumber = oi.OrderNumber WHERE o.OrderOpen = TRUE AND oi.LineType <> 'X' AND (oi.IsDropShipping IS NULL OR oi.IsDropShipping = FALSE) AND o.OrderType <> 'F' AND oi.Shipped > 0 \
        GROUP BY oi.PartID) coo ON p.PartID = coo.PartID WHERE p.RecordActive = TRUE AND p.ItemIsKit = FALSE AND plc.PLC + ' ' + p.PartNumber = ?";

HP_SQL_2 = "SELECT trim(plc.PLC + ' ' + p.PartNumber), FLOOR(IFNULL(p.OnHand, 0) - IFNULL(coo.CommittedOnOrders, 0)) FROM Plc plc \
        INNER JOIN Imaster p ON plc.PLCID = p.PLCID LEFT JOIN ( SELECT oi.PartID, SUM(oi.Shipped) AS CommittedOnOrders FROM SalesOrder so INNER JOIN [Order] o on so.OrderNumber = o.OrderNumber \
        INNER JOIN OrderItem oi ON o.OrderNumber = oi.OrderNumber WHERE o.OrderOpen = TRUE AND oi.LineType <> 'X' AND (oi.IsDropShipping IS NULL OR oi.IsDropShipping = FALSE) AND o.OrderType <> 'F' AND oi.Shipped > 0 \
        GROUP BY oi.PartID) coo ON p.PartID = coo.PartID WHERE p.RecordActive = TRUE AND p.ItemIsKit = FALSE AND (PLC.PLC = 'GFU' OR PLC.PLC = 'FMP' OR PLC.PLC = 'AVS' OR PLC.PLC = 'BLM' OR PLC.PLC = 'BUS' OR PLC.PLC = 'LND' \
	OR PLC.PLC = 'RPG' OR PLC.PLC = 'RNL' OR PLC.PLC = 'STA' OR PLC.PLC = 'FLO' OR PLC.PLC = 'BMM' OR PLC.PLC = 'HUR' OR PLC.PLC = 'DEL' OR PLC.PLC = 'LAZ' OR PLC.PLC = 'MAG' OR PLC.PLC = 'PUT') \
	AND (p.ExportToEbay = 1 OR p.ExportToAmazon = 1 OR p.Is_On_Magento = TRUE) ORDER BY plc.PLC, p.PartNumber";

SIXBIX_SQL = "Select SixBit_KMJPERFORMANCE.dbo.Listings.ListingID, SixBit_KMJPERFORMANCE.dbo.Inventory.SKU, SixBit_KMJPERFORMANCE.dbo.Inventory.InventoryID, SixBit_KMJPERFORMANCE.dbo.Inventory.QtyUncommitted, \
        SixBit_KMJPERFORMANCE.dbo.Listings.QtyRemaining From SixBit_KMJPERFORMANCE.dbo.Inventory Inner Join SixBit_KMJPERFORMANCE.dbo.Listings On Listings.ItemID = Inventory.ItemID \
        Where Listings.StatusID = 2000 AND ( Inventory.SKU like 'GFU%' OR Inventory.SKU like 'FMP%' OR Inventory.SKU like 'MAG%' OR Inventory.SKU like 'PUT%' OR Inventory.SKU like 'STA%') ORDER BY SKU";

#sixbit_result = run_sixbit_sql_statement(SIXBIT_ODBC_CONN, SIXBIX_SQL)
'''
sixbit_result = []

for row in sixbit_result:
    sku = row[1]

    hp_result = run_hp_sql_statement(HP_ODBC_CONN, HP_SQL, sku)

    quantity =  0
    for row in hp_result:
        quantity = row[0]

    print( sku + ' --> ' + str(quantity) )
''' 

hp_result = run_hp_sql_statement(HP_ODBC_CONN, HP_SQL_2)

SKU_TEST = 'STA BRC2010'

HP_Quantity = ''

for row in hp_result:
    #print(row['sku'], row['quantity'])
    if SKU_TEST in row['SKU']:
        HP_Quantity = row['Quantity'])

print ('This script executed successfully')
print ('This script will close in 5 seconds')
time.sleep(1)
print ('1..')
time.sleep(1)
print ('2..')
time.sleep(1)
print ('3..')
time.sleep(1)
print ('4..')
time.sleep(1)
print ('5..')
