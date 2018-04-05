import pyodbc
import csv
import time

def open_odbc_connection(DSN,UID,PWD):
    return pyodbc.connect('DSN='+DSN+';UID='+UID+';PWD='+PWD+';')

def run_sql_statement(ODBC_CONN,SQL, SQL_VAR_1, SQL_VAR_2, SQL_VAR_3):
    CUR_OBJ = ODBC_CONN.cursor()
    print('cursor created')
    #execute SQL statement
    CUR_OBJ.execute(SQL, (SQL_VAR_1, SQL_VAR_2, SQL_VAR_3))
    print ('update ran')
    ODBC_CONN.commit()
    print ('committed')

def run_sql_update_statement(ODBC_CONN,SQL, SQL_VAR_1, SQL_VAR_2):
    CUR_OBJ = ODBC_CONN.cursor()
    print('cursor created')
    #execute SQL statement
    CUR_OBJ.execute(SQL, (SQL_VAR_1, SQL_VAR_2))
    print('update ran')
    ODBC_CONN.commit()
    print('committed')
        

# Change the stuff below this text
CSV_TO_READ = 'updateSixbitQuantitiesByListingID_RCR.csv'  # This assumes your part numbers are in the first column
CSV_TO_READ_DEL = '\t'   # The delimiter on the CSV you are reading
ODBC_CONN_NAME = 'SixBit'                   # The ODBC connection name
ODBC_USER = 'sa_sb'                         # The ODBC user name, '' if there is no user required
ODBC_PASS = 'S1xb1tR0x'                     # The ODBC pass, '' if there is no password required
# Change the stuff above this text

#SQL Statement to get Fitment Info
ODBC_CONN = open_odbc_connection(ODBC_CONN_NAME,ODBC_USER,ODBC_PASS)

#Open CSV file
csv_Sixbit = csv.reader(open(CSV_TO_READ), delimiter=CSV_TO_READ_DEL)

#skip header row
next(csv_Sixbit, None)

#run through CSV by row
for row in csv_Sixbit:
    ListingID = row[0]
    SKU = row[1]
    InventoryID = row[2]
    QtyUncommited = row[3]
    Quantity = row[4]

    if ( int(Quantity) > int(QtyUncommited) ):
        print(SKU + ' adding inventory ')
        run_sql_update_statement(ODBC_CONN,"INSERT INTO SixBit_RACERS.dbo.Purchases (InventoryID, Quantity, PurchaseSource) VALUES (?, ?, 27)", InventoryID, Quantity)
            
    print(SKU + ' --> ' + Quantity)

    OutOfStock = 1

    if ( int(Quantity) == 0 ):
        OutOfStock = 1
        print(SKU + ' --> OutOfStock')
    else:
        OutOfStock = 0
    
    #make call to database
    run_sql_statement(ODBC_CONN,"UPDATE SixBit_RACERS.dbo.Listings SET RevisionPending = 1, QtyToList = NumberSold + ?, OutOfStock = ? WHERE ListingID = ?", Quantity, OutOfStock, ListingID)
 

print('This script executed successfully')
print('This script will close in 5 seconds')
time.sleep(1)
print('1..')
time.sleep(1)
print('2..')
time.sleep(1)
print('3..')
time.sleep(1)
print('4..')
time.sleep(1)
print('5..')

