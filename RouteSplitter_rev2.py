'''
Created on 8 Aug 2017

@author: David Fottrell

The purpose of this script is to split out Xiaoxia's Stop to Stop data into individual routes.  Rather than try to build 1 single Excel 
sheet with all data in it, this script seeks to open each week individually and append the data to the dataframe, before processing 
as per the original procedure.  

Each weeks data containing stop level records contains approximately 9 million rows of data.  We encounter memory errors trying to
work with dataframes this big, never mind concatenated files for a whole month.  As a result, we decided to split the bus routes into
a separate dataframe and store them as CSV's for modelling later.

The reason for two basic functions is that the Week 1 function creates the CSV's.  The other function appends the same CSV's created 
in week 2- 4.

'''
import gc
import pandas as pd
#import feather as ft

def main():
    #week1()
    week2Plus()
    print("Program end!!")
    return

def week1():    
    counter = 1
    # Create the dataframe with Xiaoxia's data & drop unnecessary columns
    print("Starting to read base dataframe for week 1...")
    #df = pd.read_csv('C:\\Users\\User\\Desktop\\Research Project\\Data\\Stop to Stop\\Week2_avg.csv')
    df = pd.read_csv('C:\\Users\\User\\Desktop\\Research Project\\Data\\Stop to Stop\\Week' + str(counter) +'_avg.csv')
    df.drop('Unnamed: 0', axis = 1, inplace=True)
    df.drop('UnixTimestamp', axis = 1, inplace=True)
    df.drop('Day_of_Week', axis = 1, inplace=True)
    
    # Initialise the tuple with all of the individual bus routes
    t1 = df.BusRoute.unique()
    zip(t1)
    
    print("Starting to extract Week 1 bus routes to CSV...")
    
    # For loop to iterate through each of the routes
    for i in t1:
        name = 'BR' + str(i)
        print("Starting on route", i)
        df1 = df[df.BusRoute == i]
        df1.to_csv('C:\\Users\\User\\Desktop\\Research Project\\Data\\Stop to Stop\\Bus Route CSV\\' + name + '.csv')
        gc.collect()
        df1.drop(df1.index, inplace = True)
    # This next line purges the dataframe to prevent cross contamination when reused
    df.drop(df.index, inplace = True)
    print("Finished extracting bus routes for week 1...")
    return

def week2Plus():
    counter = 3
    for j in range(2):
        print('Starting to read base dataframe for week' + str(counter) + '...')
        #df = pd.read_csv('C:\\Users\\User\\Desktop\\Research Project\\Data\\Stop to Stop\\Week' + str(counter) +'_avg.csv')
        df = pd.read_csv('C:\\Users\\User\\Desktop\\Research Project\\Data\\Stop to Stop\\Week' + str(counter) +'_avg.csv')
        df.drop('Unnamed: 0', axis = 1, inplace=True)
        df.drop('UnixTimestamp', axis = 1, inplace=True)
        df.drop('Day_of_Week', axis = 1, inplace=True)
    
        # Initialise the tuple with all of the individual bus routes
        t1 = df.BusRoute.unique()
        zip(t1)
        
        print('Starting to extract Week' + str(counter) + 'bus routes to CSV...')
        
        # For loop to iterate through each of the routes
        for k in t1:
            name = 'BR' + str(k)
            print('Starting on route', k)
            df1 = df[df.BusRoute == k]
            # This file write is different because we are trying t append data to files which now already exist
            with open ('C:\\Users\\User\\Desktop\\Research Project\\Data\\Stop to Stop\\Bus Route CSV\\' + name + '.csv', 'a') as f:
                df1.to_csv(f, header = False)
            df1.drop(df1.index, inplace = True)
        # These next 2 lines purges the data frames to prevent cross contamination when reused
        df.drop(df.index, inplace = True)
        df1.drop(df1.index, inplace = True)
        gc.collect()
        print('Finished extracting bus routes for week' + str(counter) + '...')
        counter += 1
        

    return

if __name__ == '__main__':
    main()