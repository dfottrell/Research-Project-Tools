This is a list of files I used during the machine learning phase of the Dublin Bus journey time predictor project for UCD MSc Computer Science (Conversion), 2016 project.

NovCSVMerge.py

The aim is to apply a merge and clean to all the November 2012 GPS data prior to being merged into chunks of 1 week.  The reason 
for this approach is to preserve memory, previously all attempts to process this data in chunks larger than 1 day caused memory
errors.

JanCSVMerge.py

The purpose of this script is to import January 2013 GPS data for the dublin bus fleet.  The November script will serve as a template,
but it is not totally suitable due to the data being in a GZ format.  This script will unzip each file first and then proceed to process the files in an identical manner to the process used for November data import.

SummaryGPS.py

This program summarises of the all of the November and January GPS bus data and synchronised that data with the weather (Wet or Dry) 
at that time.  This program takes in that data and performs 2 additional, main, steps.  First, after preprocessing, it generates journey duration times.  Secondly, it assigns a day of the week value before finally outputting the finished file to a new CSV.  Finally, it removes journeys less than 10 minutes in duration.  This may seem long winded, but it memory constraints dictate this being done in this 
manner.

12c+-+Single+Random+Forest+Regressor+Analaysis+of+Summary+Data (1).ipynb

This is a JUPYTER notebook which was used to build a single RF model based on the Analytics Base Table (ABT) generated from CSVMerge scripts and SummaryGPS.py script.

RouteSplitter_rev2.py

The purpose of this script is to split out Xiaoxia's Stop to Stop data into individual routes.  Rather than try to build 1 single Excel 
sheet with all data in it, this script seeks to open each week individually and append the data to the dataframe, before processing 
as per the original procedure.  

Each weeks data containing stop level records contains approximately 9 million rows of data.  We encounter memory errors trying to
work with dataframes this big, never mind concatenated files for a whole month.  As a result, we decided to split the bus routes into
a separate dataframe and store them as CSV's for modelling later.

RandomForestModelBuilder.py

The purpose of this file is to build a Random Forest (RF) model for every bus route in Dublin based on the summary GPS data for 
November 2012.  Each route has been separated into route specific chunks of data in CSV format named according to their route, this 
script will go through those CSV's and use them to build a model.  Each model will be stored in a seperate location, for use later.  This script will also output the OOB score for each model to a separate CSV file for analysis later. 

