'''
Created on 11 Aug 2017

@author: David Fottrell

The purpose of this file is to build a Random Forest (RF) model for every bus route in Dublin based on the summary GPS data for 
November 2012.  Each route has been separated into route specific chunks of data in CSV format named according to their route, this 
script will go through those CSV's and use them to build a model.

Each model will be stored in a seperate location, for use later.  This script will also output the OOB score for each model to a 
separate CSV file for analysis later. 

This process was prototyped in JUPYTER notebook, see file STS1f.

'''

import datetime
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
from sklearn.metrics import mean_squared_error
from sklearn.externals import joblib
import os
import gc

def main():
    print("Starting to build Random Forest Models for each bus route...")
    buildRFModel()
    print("Program complete!!")
    return

def routeList():    
    '''
    The purpose of this function is generate the list of all bus routes in a tuple, this list can then be used later to control a 
    for loop which builds the RF models for each route.
    '''
    print("Compiling route list...")
    #df = pd.read_csv('C:\\Users\\User\\Desktop\\Research Project\\Data\\Stop to Stop\\Week2_avg.csv')
    df = pd.read_csv('C:\\Users\\User\\Desktop\\Research Project\\Data\\Stop to Stop\\BusDepartures_all.csv')
    t1 = df.Route.unique()
    zip(t1)
    return t1

def formatFrame(frm):
    '''
    THe purpose of this function is to pre format dataframe prior to merging with weather data 
    '''
    print("Formatting dataframe...")
    df = frm
    df.drop('Unnamed: 0', axis = 1, inplace=True)
    df['LogTime'] = pd.to_datetime(df['LogTime'])
    # We need to create a new column called Date which normalises Timestamp to nearest hour, used to synhronise with weather data
    df['Date'] = pd.DatetimeIndex(df['LogTime'])
    # Want to rename the columns to more easily fit my code and reduce the amount of typing / cutting & pasting
    df.columns = ['JID', 'StopID', 'LogTime', 'BusRoute', 'Date']
    # Reformat the data column to match the nearest hour, which will synchronise with the raw sMet Eireann data
    df['Date'] = df['Date'].apply(lambda x: x.replace(minute=0, second=0))
    print("Finished formatting dataframe...")
    return df

def mergeWeather(frm):
    '''
    This function merges rainfall data with the main dataframe
    '''
    print("Merging weather...")
    df = frm
    df_rain = pd.read_csv('C:\\Users\\User\\Desktop\\Research Project\\Data\\SQL Scripts\\Nov 2012 Rainfall.csv')
    # Date is in wrong format, need to change to datetime format
    df_rain['Date'] = pd.to_datetime(df_rain['Date'])
    # Merge these the weather with the GPS data & export to external file
    df_merged = pd.merge(df, df_rain, on='Date', how='outer')
    # Want to generate statement of wet or dry depending on amount of rain
    df_merged['Weather (1 = W, 0 = D)'] = np.where(df_merged['rain'] > 0, 1, 0)
    # Drop redundant columns
    df_merged.drop('Date', axis = 1, inplace=True)
    df_merged.drop('rain', axis = 1, inplace=True)
    # Convert days to coded values, 0 = Monday, 6 = Sunday...helps reduce dummy columns during RF modelling
    df_merged['Day'] = df_merged['LogTime'].dt.weekday    
    df_merged = df_merged.dropna()
    df_merged['JID'] = df_merged['JID'].astype(int)
    df_merged['StopID'] = df_merged['StopID'].astype(int)
    df_merged['Day'] = df_merged['Day'].astype(int)
    df_merged['BusRoute'] = df_merged['BusRoute'].astype('category')
    print("Finised merging weather...")
    return df_merged

def mergeDepartureTimes(frm, route):
    '''
    The purpose of this function is to calculate the arrival times at each stop, then merge the unique departure times associated
    with each route / journey combination
    '''
    print("Merging departure time information...")
    df_merged = frm
    df_duration = df_merged.groupby(['Day', 'JID', 'StopID', 'Weather (1 = W, 0 = D)']).agg({'LogTime':[np.max, np.min]})
    df_duration = df_duration.sort_values(by=('LogTime', 'amin'),ascending=True)
    # Convert time series into float time to enable RF modelling
    Ahour = pd.to_datetime(df_duration[('LogTime', 'amin')]).dt.hour
    Amin = pd.to_datetime(df_duration[('LogTime', 'amin')]).dt.minute/60
    Dhour = pd.to_datetime(df_duration[('LogTime', 'amax')]).dt.hour 
    Dmin = pd.to_datetime(df_duration[('LogTime', 'amax')]).dt.minute/60    
    df_duration[('LogTime', 'amin')] = Ahour + Amin 
    df_duration[('LogTime', 'amax')] = Dhour + Dmin 
    # Idea here is to try and round the time to 2 decimal places
    df_duration.round({('LogTime', 'amin'): 2, ('LogTime', 'amax'): 2})
    
    # Reformat the dataframe to get rid of that unwieldy column format
    df_duration.to_csv('C:\\Users\\User\\Desktop\\Research Project\\Data\\Stop to Stop\\temp.csv')
    df3 = pd.read_csv('C:\\Users\\User\\Desktop\\Research Project\\Data\\Stop to Stop\\temp.csv', header = None)
    # Eliminate bad labelling in the column headers
    df3=df3.dropna(axis = 0)
    # Rebuild the column headers
    df3.columns = ['Day', 'JID', 'StopID', 'Weather (1 = W, 0 = D)', 'Departure', 'Arrival']
    df3['Day'] = df3['Day'].astype(int)
    df3['JID'] = df3['JID'].astype(int)
    df3['StopID'] = df3['StopID'].astype(int)
    df3['Weather (1 = W, 0 = D)'] = df3['Weather (1 = W, 0 = D)'].astype(int)
    df3['Arrival'] = df3['Arrival'].astype(float)
    df3['Departure'] = df3['Departure'].astype(float)
    # THis next section searches for all departure times by a specific route
    df2 = pd.read_csv('C:\\Users\\User\\Desktop\\Research Project\\Data\\Stop to Stop\\BusDepartures_all.csv')
    df2.drop('Day', axis = 1, inplace=True)
    # Added this line because the filter for route is not working, Route is dtype object, route is dtyp str...think thats the problem
    #df2['Route'] = df2['Route'].str.split(',')
    df2 = df2[df2.Route.str.match(route, case=True)]
    df2.drop('Route', axis = 1, inplace=True)
    # Create a new, complete data frame which will be modelled later
    df3 = df3.merge(df2, how='inner', left_on = 'JID', right_on = 'JID')
    # Format the new dataframe
    df3['Day'] = df3['Day'].astype(int)
    df3['JID'] = df3['JID'].astype(int)
    df3['StopID'] = df3['StopID'].astype(int)
    df3['Weather (1 = W, 0 = D)'] = df3['Weather (1 = W, 0 = D)'].astype(int)
    df3['Arrival'] = df3['Arrival'].astype(float)
    df3['Departure'] = df3['Departure'].astype(float)
    df3['Departure Time'] = df3['Departure Time'].astype(float)
    print("Finished merging departure time information...")
    return df3

def buildRFModel(): 
    '''
    The purpose of this function is to loop through the CSV's for each bus route and use that to build an Random Forest model. The model
    will predict the arrival time at any stop the users wants to get on the bus, and the the time the bus arrives at any stop along
    that route.
    
    The function will also output the Mean Squared Error (MSE) and Out of Bag (OOB) score for each model to a file for reference later.
    This will help determine the performance of each model when compared to real data later.     
    '''
    t1 = routeList()
    count = len(t1)
    for i in range (count):
        name = 'BR' + str(t1[i])
        print("Starting to build model for route", str(t1[i]))
        df = pd.read_csv('C:\\Users\\User\\Desktop\\Research Project\\Data\\Stop to Stop\\Bus Route CSV\\' + name + '.csv')
        
        # Adding this because some of the raw data has nulls in it, discovered in Route 007 data
        df['StopID'].replace('null', np.nan, inplace=True)
        df.dropna(subset=['StopID'], inplace=True)
        
        # Formatting data prior to modelling
        df = formatFrame(df)
        dfW = mergeWeather(df)
        dfDT = mergeDepartureTimes(dfW, t1[i])
        
        # Prepare dataframe for modeeling
        df_cont_feat = dfDT[['Day' ,'Departure Time', 'StopID','Weather (1 = W, 0 = D)']]
        frames = [df_cont_feat]
        result = pd.concat(frames, axis =1, copy = False) 
        
        # This section calculates the size of the training data, this is an automated way of getting 70% of rows for RF fitting
        # Create a tuple based on the result of the shape command, returns 2 dimensional array
        t2 = result.shape
        # Index 0 in the array has the number of rows
        rows = t2[0]
        # Calculate a rounded integer which is 70% of the rows
        train_rows = int(rows * 0.7)
        test_rows = (rows - train_rows)
        
        # We will use 70% for training and 30% for testing
        df_train = result[:train_rows]
        df_test = result[test_rows:]
        
        # Train RF with 50 trees
        rfc = RandomForestRegressor(n_estimators=50, oob_score=True)
        X = df_train
        y = dfDT.Arrival[:train_rows]
        test_y = dfDT.Arrival[test_rows:]
        
        # Fit random model on test dataset
        rfc.fit(X, y)
        
        # Test the model
        preds = rfc.predict(df_test)
        MSE = mean_squared_error(test_y, preds)
        OOB = rfc.oob_score_
        
        # Write the results to a log file for analysis later
        with open ('C:\\Users\\User\\Desktop\\Research Project\\Data\\Stop to Stop\\Route Models\\Score.txt', 'a') as f:
            f.write(str(name) + ',' + str(MSE) + ',' + str(OOB) + '\n')
            f.close()
        
        # Write the model to an external file for use later
        filename = 'C:\\Users\\User\\Desktop\\Research Project\\Data\\Stop to Stop\\Route Models\\RF' + name + '_v0.1.mdl'
        joblib.dump(rfc, filename)
        
        # Clean up the dataframes prior to reuse, to prevent data contamination and also manage memory
        gc.collect()
        df.drop(df.index, inplace = True)
        dfW.drop(dfW.index, inplace = True)
        dfDT.drop(dfDT.index, inplace = True)
        result.drop(result.index, inplace = True)
        
        # Finished
        print("Finished building model for route", t1[i])
    return

if __name__ == '__main__':
    main()