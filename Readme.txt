This is a list of files I used during the machine learning phase of the Dublin Bus journey time predictor project for UCD MSc Computer Science (Conversion), 2016 project.

The user should already have downloaded the raw Dublin Bus Noveber 2012 & January 2013 GPS data to their local machine.  Before running these scripts, the user should update the file paths in the scripts to match their local directory structure.  The scripts should be run in order, within ECLIPSE.

Single RF Model Scripts
-----------------------
1. NovCSVMerge.py

The aim is to apply a merge and clean to all the November 2012 GPS data prior to being merged into chunks of 1 week.  The reason 
for this approach is to preserve memory, previously all attempts to process this data in chunks larger than 1 day caused memory
errors.

2. JanCSVMerge.py

The purpose of this script is to import January 2013 GPS data for the dublin bus fleet.  The November script will serve as a template,
but it is not totally suitable due to the data being in a GZ format.  This script will unzip each file first and then proceed to process the files in an identical manner to the process used for November data import.

3. SummaryGPS.py

This program summarises of the all of the November and January GPS bus data and synchronised that data with the weather (Wet or Dry) 
at that time.  This program takes in that data and performs 2 additional, main, steps.  First, after preprocessing, it generates journey duration times.  Secondly, it assigns a day of the week value before finally outputting the finished file to a new CSV.  Finally, it removes journeys less than 10 minutes in duration.  This may seem long winded, but it memory constraints dictate this being done in this 
manner.

4. 12c+-+Single+Random+Forest+Regressor+Analaysis+of+Summary+Data (1).ipynb

This is a JUPYTER notebook which was used to build a single RF model based on the Analytics Base Table (ABT) generated from CSVMerge scripts and SummaryGPS.py script.


Stop to Stop RF Model Scripts
-----------------------------
Note 1: You will need access to 4 Excel spreadsheets with raw summary stop to stop data in them for these scripts to run properly.  This totals 2.2GB, even zipped it is 311MB and beyond the limits allowed either by MOODLE or GitHub.  Please send me your email address if you want these files in order to test the scripts.  I will facilitate by creating a shared DROPBOX for you to access the files.

Note2: You will need to change the file paths to match your own file locations in each script.

Note3: All scripts were written in PYTHON 3.5 and executed in ECLIPSE.  Run these scripts in order below.  


Thank you in advance...David Fottrell


1. RouteSplitter_rev2.py

The purpose of this script is to split out 4 Excel files with Stop to Stop data into individual routes.  Rather than try to build 1 single Excel sheet with all data in it, this script seeks to open each week individually and append the data to a route specific dataframe, before saving that route specific dataframe to an external CSV file.  

2. RandomForestModelBuilder.py

This file builds on the previous script and creates a Random Forest (RF) model for every bus route in Dublin based on the route specific CSV.  Each model will be stored in a seperate location, for use later.  This script will also output the OOB score for each model to a separate CSV file for analysis later. 

