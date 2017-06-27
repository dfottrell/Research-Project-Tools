The purpose of these files is to enable easier handling of large CSV files (in excess of 3.5GB) for my research project at University College Dublin.  The CSVMerge.py program scans a directory in which I have approximately 30 CSV files, circa 150MB each and appends them into one single file.

The SQL script, GPS_Data_Read was developed to allow a fast upload of the CSV files mentioned above into MySQL.  The import wizard was taking in excess of 24 hours to read in a 150MB file.  This script reduces that time to <40 seconds.
