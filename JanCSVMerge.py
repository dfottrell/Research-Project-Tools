'''
Created on 21 Jul 2017

@author: David Fottrell 

The purpose of this script is to import January 2013 GPS data for the dublin bus fleet.  The November script will serve as a template,
but it is not totally suitable due to the data being in a GZ format.

This script will unzip each file first and then proceed to process the files in an identical manner to the process used for November
data import.

Followup processing will be required, similar to that used in NovSummary.py script.  Only then will November & January datasets be
merged into one Summary CSV.

@attention: Updated 27th July
Due to issues with pd.concat during the data analytics phase of this project, it became necessary to change the way weather data was
displayed.  Instead of a simple wet or dry, I changed it to 1 for wet or 0 for dry.

The hope is that this will mean we need less dummies categories in the machine learning work later on.  Currently, the requirement
for dummies under the old system added >15,600 extra columns.  This meant we could not effectively model more than 5000 rows of data.

'''

import os
import gc
import numpy as np
import pandas as pd
import gzip
import shutil

file_list = os.listdir('C:\\Users\\User\\Desktop\\Research Project\\Data\\January 2013 GPS Data') # dir is your directory path
number_files = len(file_list)


def main():
    Unzip()
    JanCSVMerge()
    #CSVClean()
    print("Program complete!!")
    return

def Unzip():
    # This function decompresses the files from GZ format to a regular CSV in the parent directory
    print("Decompressing raw data...")
    for num in range(number_files):
        dt = 20130101 + num
        log = "siri." + str(dt)
        with gzip.open('C:\\Users\\User\\Desktop\\Research Project\\Data\\January 2013 GPS Data\\' + log + '.csv.gz', 'rb') as f_in, open('C:\\Users\\User\\Desktop\\Research Project\\Data\\January 2013 GPS Data\\' + log + '.csv', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    print("Finished decompressing raw data...")
    return

def JanCSVMerge():
    Week = 1
    counter = 1
    # Repeat the above for remaining files in directory and append result to CSV created above
    for num in range(number_files - 1):
        if counter %7 == 0 :
            Week += 1

        print("Working on file ", counter)
        
        # File import phase
        dt = 20130101 + num
        log = "siri." + str(dt)
        df = pd.read_csv('C:\\Users\\User\\Desktop\\Research Project\\Data\\January 2013 GPS Data\\' + log + '.csv', sep = ',', header = None)
        df.columns = ['UNIXTimestamp', 'Route', 'Direction', 'PatternID', 'GPSDate', 'VehicleJourneyID', 'Operator', 'Congestion', 'Longitude', 'Latitude', 'Delay', 'BlockID', 'VehicleID', 'StopID', 'AtStop']
        
        # Remove needless data
        df = df.drop_duplicates()
        df = df[df.PatternID != 'null']
        
        # Create new columns for later calculations
        df['LogTime'] = pd.to_datetime(df['UNIXTimestamp'],unit='us')
        df['Date'] = df['LogTime'].apply(lambda x: x.replace(minute=0, second=0))
        df['Bus Route'] = df.PatternID.str[:4]
        
        # After creating the extra columns above, remove columns not going to be used, makes resulting file less cumbersome
        print("Starting data clean up...")
        #df.drop('Unnamed: 0', axis = 1, inplace=True)
        df.drop('UNIXTimestamp', axis = 1, inplace=True)
        df.drop('Route', axis = 1, inplace=True)
        df.drop('Congestion', axis = 1, inplace=True)
        df.drop('VehicleID', axis = 1, inplace=True)
        df.drop('Direction', axis = 1, inplace=True) 
        df.drop('Operator', axis = 1, inplace=True) 
        df.drop('Longitude', axis = 1, inplace=True)
        df.drop('Latitude', axis = 1, inplace=True)
        df.drop('BlockID', axis = 1, inplace=True)
        df.drop('AtStop', axis = 1, inplace=True)  
        df.drop('PatternID', axis = 1, inplace=True)
        df.drop('GPSDate', axis = 1, inplace=True) 
        df.drop('Delay', axis = 1, inplace=True) 
        print("Finished data clean up!")

        print("Merging with weather data...")
        # Read in November data for rainfall
        df_rain = pd.read_csv('C:\\Users\\User\\Desktop\\Research Project\\Data\\SQL Scripts\\Jan 2013 Rainfall.csv')
        
        # Date is in wrong format, need to change to datetime format
        df_rain['Date'] = pd.to_datetime(df_rain['Date'])
        
        # Merge these the weather with the GPS data & export to external file
        df_merged = pd.merge(df, df_rain, on='Date', how='outer')
        #df_merged.columns = ['VehicleJourneyID', 'StopID', 'LogTime', 'Date', 'Bus Route', 'Rain']
        
        # Want to generate statement of wet or dry depending on amount of rain
        df_merged['Weather (1 = W, 0 = D)'] = np.where(df_merged['rain'] > 0, 1, 0)
        df_merged.drop('Date', axis = 1, inplace=True)
        df_merged.drop('rain', axis = 1, inplace=True)
        
        # Write resulting dataframe to a new CSV file   
        with open('C:\\Users\\User\\Desktop\\Research Project\\Data\\JanABTWeek' + str(Week) +'.csv', 'a') as f:
            df_merged.to_csv(f, header=False)
        print("Finished file")
        counter += 1
        gc.collect()
    print("Merge process complete!")
    return
'''
def CSVClean():
    print("Beginning clean up...")
    os.remove("C:\\Users\\User\\Desktop\\Research Project\\Data\\January 2013 GPS Data\\*.csv")
    print("Finished clean up...")
    print("Program Complete!")
    return
'''
if __name__ == '__main__':
    main()