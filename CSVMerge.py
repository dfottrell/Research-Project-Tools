'''
Created on 25 Jun 2017

@author: David Fottrell

This is intended to merge multiple CSV files together for the Research Project in MSc Computer Science (Conversion), UCD

There are CSV files containing Dublin Bus GSP data for November 2012 and January 2013 which need to be merged into one
CSV file as a prerequisite to modeling the data.

Purpose of this code is to compile all of the November GPS data into one CSV file.  It does this by starting with one file, 
then opening all of the other files in the directory and appending them to the first file.  Then the result file gets a 
header row and is then saved as a separate CSV


'''
import os

file_list = os.listdir('C:\\Users\\User\\Desktop\\Research Project\\Data\\November 2012 GPS Data') # dir is your directory path
number_files = len(file_list)

def main():
    CSVMerge()
    return

def CSVMerge():
    fout = open('C:\\Users\\User\\Desktop\\Research Project\\Data\\SummaryGPSData2.csv', 'a')
    for num in range(number_files):
        dt = 20121106 + num
        log = "siri." + str(dt)
        for line in open('C:\\Users\\User\\Desktop\\Research Project\\Data\\November 2012 GPS Data\\' + log + '.csv'):
            fout.write(line)    
    fout.close()
    return

if __name__ == '__main__':
    main()