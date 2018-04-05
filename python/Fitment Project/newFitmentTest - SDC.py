# https://stackoverflow.com/questions/11322430/how-to-send-post-request
# https://docs.python.org/3.4/howto/urllib2.html
# https://stackoverflow.com/questions/10973614/convert-json-array-to-python-list - json array
# https://stackoverflow.com/questions/1523660/how-to-print-a-list-in-python-nicely - print array nicely
# https://stackoverflow.com/questions/1653591/python-urllib2-response-header - get response.info specific header
# https://stackoverflow.com/questions/663171/is-there-a-way-to-substring-a-string-in-python - substring( slicing)
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json
import csv
import time

CSV_TO_READ = 'SKUs_without_Fitments_SDC.csv'

CSV_TO_READ_DEL = ','
CSV_TO_WRITE = 'Sixbit_' + time.strftime('%m%d') + '-Fitments_To_Add_SDC.csv'
CSV_TO_WRITE_DEL = ','

out_file = open(CSV_TO_WRITE, "w",newline='')
new_sku_csv = csv.writer(out_file,delimiter=CSV_TO_WRITE_DEL)
print("Creating New Fitments_To_Add_SDC.csv")

rateLimit = 60

approvedLines = {"ACI" : "BDDP",
                 "AFS" : "BGPL",
                 "AMP" : "BGQD",
                 "AVS" : "BBFF",
                 "BDW" : "FMJR",
                 "BMM" : "BBFT",
                 "BRG" : "BRLQ",
                 "BUS" : "BDMQ",
                 "CGT" : "BJNS",
                 "CTN" : "FKDX",
                 "DGH" : "BKLK",
                 "DHA" : "CNSQ",
                 "DMN" : "BGWW",
                 "EDG" : "BKDQ",
                 "EIB" : "DMWF",
                 "ENE" : "BDVQ",
                 "ERL" : "CFRL",
                 "FLO" : "BDXN",
                 "FLT" : "CJWH",
                 "FRO" : "GSKG",
                 "HAY" : "BCCR",
                 "HKR" : "BBVM",
                 "HOL" : "BBVL",
                 "HSK" : "BBVR",
                 "HUR" : "BCCS",
                 "HYT" : "BFFP",
                 "JBA" : "FBKB",
                 "JET" : "BHDL",
                 "LND" : "BFKJ",
                 "LWI" : "BCCT",
                 "MAL" : "BFKR",
                 "MEL" : "BCBC",
                 "MOT" : "BHHD",
                 "MRG" : "BCZG",
                 "MSD" : "BCCX",
                 "NOR" : "CLSN",
                 "PEP" : "BKLJ",
                 "PRT" : "BHLP",
                 "PTX" : "BHKK",
                 "QA1" : "BJGM",
                 "RDL" : "BKMQ",
                 "RNL" : "CLRJ",
                 "ROF" : "GMVN",
                 "RPG" : "CLSG",
                 "STA" : "BHPC",
                 "TRX" : "BKHI",
                 "WEI" : "BHTK"
                 }
                 
with open(CSV_TO_READ) as f: # Open the csv
    cr = csv.reader(f, delimiter=CSV_TO_READ_DEL) # Set the delimiter on the CSV
    for column in cr:  # Scan through the rows in the CSV
        toWrite = []
        print(" --------------------------------------- ")

        print("SKU: " + column[0])
        print("")

        #get aaia code for lines
        plc = column[0][:3]
        partNumber = column[0][4:]
        
        try:
            aaiaCode = approvedLines[plc]
            #print(aaiaCode)

            # Set destination URL here
            url = 'http://sdc.semadatacoop.org/sdcapi/lookup/vehiclesbyproduct'
            # Set POST fields here
            post_fields = {'token' : 'EAAAAOzGy0qBZXM/lWbuwAEzg0fEsR+OMcU+aB5r1oiOpvVh',
                'aaia_brandid' : aaiaCode,
                'partNumber' : partNumber }     
            #get Fitments for SKU in CSV

            if rateLimit < 2:
                print("Rate Limit reached. Waiting 60 seconds.")
                time.sleep(60)
            
            request = Request(url, urlencode(post_fields).encode())
            #json_data = urlopen(request).read().decode()

            with urlopen(request) as response:
                # gets the url requests
                the_page = response.info()
                print(the_page)
                # gets the ratelimit-remaining (Limit of 60 per minute)
                rateLimit = int(response.info()['RateLimit-Remaining'])
                json_data = response.read()
                print("Rate Limit Remaiing: " + str(rateLimit))
                print("")

            #puts into an array
            data = json.loads(json_data)
            
            #for key, value in data['Vehicles']:
            #    print (key, value)
            i = 0
            while i < len(data['Vehicles']):
                toWrite = []
                toWrite.append( str(data['Vehicles'][i]['Year']) )
                toWrite.append( data['Vehicles'][i]['MakeName'] )
                toWrite.append( data['Vehicles'][i]['ModelName'] )
                toWrite.append( data['Vehicles'][i]['SubmodelName'] )
                toWrite.append( column[0] )
                
                print(str(data['Vehicles'][i]['Year']) + ' ' + data['Vehicles'][i]['MakeName']
                    + ' ' + data['Vehicles'][i]['ModelName'] + ' ' + data['Vehicles'][i]['SubmodelName'])
                i += 1

                #print(toWrite)

                new_sku_csv.writerow(toWrite)
            
        except KeyError:
        #except ValueError:
            print("No PLC match.")
            continue
    f.close()
    out_file.close()
    
print(" --------------------------------------- ")
print('This script executed successfully')
print('This script will close in 5 seconds')
time.sleep(1)
print('5..')
time.sleep(1)
print('4..')
time.sleep(1)
print('3..')
time.sleep(1)
print('2..')
time.sleep(1)
print('1..')
