import mysql.connector
from mysql.connector import errorcode
import csv
import time


# Change the stuff below this text
PLC_CODE = 'AVS'                            # PLC we are checking
CSV_TO_READ = 'SKUs_without_Fitments.csv'   # This assumes your part numbers are in the first column
                                            # Also your parts have the PLC and Part Number
                                            # ie. LND EX-0122-07.
CSV_TO_READ_DEL = '\t'                      # The delimer on the CSV you are reading
CSV_TO_WRITE = 'MySQL_' + time.strftime('%m%d') + '_Fitments_To_Add_Deleted_.csv'        # Name of the CSV we will output the part numbers too
CSV_TO_WRITE_DEL = ','                      # The delimiter you would like to use on the output CSV
ODBC_CONN_NAME = 'SixBit'                   # The ODBC connection name
ODBC_USER = 'sa_sb'                         # The ODBC user name, '' if there is no user required
ODBC_PASS = 'S1xb1tR0x'                     # The ODBC pass, '' if there is no password required
# Change the stuff above this text

out_file = open(CSV_TO_WRITE, "w",newline='')
new_sku_csv = csv.writer(out_file,delimiter=CSV_TO_WRITE_DEL)

cnx = mysql.connector.connect(user='kmjentco',
                                  password='Th3_Hu1k',
                                  host='198.154.228.18',
                                  database='kmjentco_ssq1')

query = ( "SELECT sku, year, make, model, trim, engine "
                      "FROM fitment_search "
                      "WHERE sku = %s "
                      "ORDER BY sku")

try:
    with open(CSV_TO_READ) as f:
        cr = csv.reader(f, delimiter=CSV_TO_READ_DEL)
        for row in cr:            

            cursor = cnx.cursor()
            
            cursor.execute(query, (row[0],))

            for (sku, year, make, model, trim, engine) in cursor:
                toWrite = []
                toWrite.append(year)
                toWrite.append(make)
                toWrite.append(model)
                toWrite.append(trim)
                toWrite.append(engine)
                toWrite.append(sku)
                
                new_sku_csv.writerow(toWrite)

            print(row[0])

            cursor.close()
    f.close()
    out_file.close()
    
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cnx.close()
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
    
