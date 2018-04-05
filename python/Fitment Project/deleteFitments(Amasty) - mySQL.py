import mysql.connector
from mysql.connector import errorcode
import csv
import time


# Change the stuff below this text
PLC_CODE = 'AVS'                            # PLC we are checking
CSV_TO_READ = 'SKUs_delete_Fitments.csv'   # This assumes your part numbers are in the first column
                                            # Also your parts have the PLC and Part Number
                                            # ie. LND EX-0122-07.
CSV_TO_READ_DEL = '\t'                      # The delimer on the CSV you are reading
# Change the stuff above this text
cnx = mysql.connector.connect(user='kmjentco',
                                  password='Th3_Hu1k',
                                  host='198.154.228.18',
                                  database='kmjentco_ssq1')

query = ( "DELETE `am_finder_map` FROM `am_finder_map` WHERE `sku` = %s ")

try:
    with open(CSV_TO_READ) as f:
        cr = csv.reader(f, delimiter=CSV_TO_READ_DEL)
        for row in cr:            

            cursor = cnx.cursor()
            cursor.execute(query, (row[0],))
            print('Deleted: ' + row[0])

            cursor.close()
    f.close()
    
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cnx.commit()
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
    
