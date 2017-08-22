'''
Created on 21 Jul 2017

@author: David Fottrell

This program summarises of the all of the November and January GPS bus data and synchronised that data with the weather (Wet or Dry) 
at that time.  This program takes in that data and performs 2 additional, main, steps.  First, after preprocessing, it generates journey duration 
times.  Secondly, it assigns a day of the week value before finally outputting the finished file to a new CSV.  Finally, it removes
journeys less than 10 minutes in duration.  This may seem long winded, but it memory constraints dictate this being done in this 
manner.

@attention: Changed df['Day'] = df['DateTime'].dt.weekday_name to a variation df['Day'] = df['DateTime'].dt.weekday.  The point of this
is to encode days as numbers.  The hope is that this will mean we need less dummies categories in the machine learning work later on.  Currently, the requirement
for dummies under the old system added >15,600 extra columns.  This meant we could not effectively model more than 5000 rows of data.
 

'''

import gc
import pandas as pd
import numpy as np

def main():
    November()
    January()
    print("Program complete")
    return

def November():
    for Week in range (1, 5):
        print("Starting November on week ", Week)
        # The dtype statement is intended to minimise the amount of memory and, hopefully, stop memory errors!
        print("\tReading in CSV...")
        df = pd.read_csv('C:\\Users\\User\\Desktop\\Research Project\\Data\\NovABTWeek' + str(Week) +'.csv', header = None, dtype = {1:object, 2:object, 3:object, 4:object, 5:object})
        
        # This statement exists because the reading in process adds another indexing column
        df.drop(0, axis = 1, inplace = True)
        
        # Dataframe arrives in without any headers, this statement replaces them
        print("\tApplying headers...")
        df = df.rename(columns={1: 'JourneyID', 2:'StopID', 3: 'DateTime', 4: 'BusRoute', 5:'Weather'})
        
        # Datetypes are not conducive to calculations later, reformatting them now
        print("\tReformatting data...")
        df['DateTime'] = pd.to_datetime(df['DateTime'])
        df['JourneyID'] = df['JourneyID'].astype('category')
        df['StopID'] = df['StopID'].astype('category')
        df['BusRoute'] = df['BusRoute'].astype('category')
        df['Weather'] = df['Weather'].astype('category')
        gc.collect()
        
        # Adding in day of the week, because the original version did not have this.  Maybe useful for analytics or SQL later
        print("\tCalculating day of the week...")
        df['Day'] = df['DateTime'].dt.weekday
    
        # Aggregate the max and min journey times to enable duration calculations later
        print("\tCalculating duration of each journey...")
        df_duration = df.groupby(['Day', 'BusRoute','JourneyID', 'Weather']).agg({'DateTime':[np.max, np.min]})
        
        # Ensure date time formats are corect for later calculation
        df_duration[('DateTime', 'amax')] = pd.to_datetime(df_duration[('DateTime', 'amax')])
        df_duration[('DateTime', 'amin')] = pd.to_datetime(df_duration[('DateTime', 'amin')])
        gc.collect()
        
        # Calculate journey durations...methodology worked out in notebook 7, In[13]
        df_duration['Duration'] = (df_duration[('DateTime', 'amax')] - df_duration[('DateTime', 'amin')]) / (np.timedelta64(1, 's'))
        # Deletes all journeys less than 600 seconds (e.g. 10 minutes)...those are considered to be invalid journeys
        # Split into two statements because of memory errors if concatenated into one statement
        print("\tFiltering out journeys with durations less than 10 mins and greater than 4 hours...")
        df_duration = df_duration[(df_duration.Duration >= 600)]
        df_duration = df_duration[(df_duration.Duration <= 14400)]
        gc.collect()
        
        # Output result to a summary CSV for the month of November 
        print("\tAppending finished dataframe to summary CSV...")
        with open('C:\\Users\\User\\Desktop\\Research Project\\Data\\SummaryGPS_Rev6.csv', 'a') as f:
                df_duration.to_csv(f, header=False)
            
        
        #df_duration.to_csv('C:\\Users\\User\\Desktop\\Research Project\\Data\\NovSummary.csv')
        Week += 1
        gc.collect()
    print("November complete!!")

    return
   
def January():
    for Week in range (1, 5):
        print("Starting January on week ", Week)
        # The dtype statement is intended to minimise the amount of memory and, hopefully, stop memory errors!
        print("\tReading in CSV...")
        df = pd.read_csv('C:\\Users\\User\\Desktop\\Research Project\\Data\\JanABTWeek' + str(Week) +'.csv', header = None, dtype = {1:object, 2:object, 3:object, 4:object, 5:object})
        
        # This statement exists because the reading in process adds another indexing column
        df.drop(0, axis = 1, inplace = True)
        
        # Dataframe arrives in without any headers, this statement replaces them
        print("\tApplying headers...")
        df = df.rename(columns={1: 'JourneyID', 2:'StopID', 3: 'DateTime', 4: 'BusRoute', 5:'Weather'})
        
        # Datetypes are not conducive to calculations later, reformatting them now
        print("\tReformatting data...")
        df['DateTime'] = pd.to_datetime(df['DateTime'])
        df['JourneyID'] = df['JourneyID'].astype('category')
        df['StopID'] = df['StopID'].astype('category')
        df['BusRoute'] = df['BusRoute'].astype('category')
        df['Weather'] = df['Weather'].astype('category')
        gc.collect()
        
        # Adding in day of the week, because the original version did not have this.  Maybe useful for analytics or SQL later
        print("\tCalculating day of the week...")
        df['Day'] = df['DateTime'].dt.weekday
    
        # Aggregate the max and min journey times to enable duration calculations later
        print("\tCalculating duration of each journey...")
        df_duration = df.groupby(['Day', 'BusRoute','JourneyID', 'Weather']).agg({'DateTime':[np.max, np.min]})
        
        # Ensure date time formats are corect for later calculation
        df_duration[('DateTime', 'amax')] = pd.to_datetime(df_duration[('DateTime', 'amax')])
        df_duration[('DateTime', 'amin')] = pd.to_datetime(df_duration[('DateTime', 'amin')])
        gc.collect()
        
        # Calculate journey durations...methodology worked out in notebook 7, In[13]
        df_duration['Duration'] = (df_duration[('DateTime', 'amax')] - df_duration[('DateTime', 'amin')]) / (np.timedelta64(1, 's'))
        # Deletes all journeys less than 10 minutes and longer than 4 hrs...those are considered to be invalid journeys
        print("\tFiltering out journeys with durations less than 10 mins and greater than 4 hours...")
        df_duration = df_duration[(df_duration.Duration >= 600)]
        df_duration = df_duration[(df_duration.Duration <= 14400)]
        gc.collect()
        
        # Output result to a summary CSV for the month of November 
        print("\tAppending finished dataframe to summary CSV...")
        with open('C:\\Users\\User\\Desktop\\Research Project\\Data\\SummaryGPS_Rev6.csv', 'a') as f:
                df_duration.to_csv(f, header=False)
            
        
        #df_duration.to_csv('C:\\Users\\User\\Desktop\\Research Project\\Data\\NovSummary.csv')
        Week += 1
        gc.collect()
    print("January complete!!")
    return

if __name__ == '__main__':
    main()