#!/usr/bin/python3

#
# 2020-04-03 Version 0.2
# giulio
# uses data from COVID-19 openZH
#
# this script merges all files in the directory defined by inp_path
# initializes integer columns with 0 not with "" as with the original script does
# (it's difficult to calculate with characters ;-)
#
# example openzh/COVID_19 original merged data: 
# Data from several cantons have columns with integer values that are initialized as strings ""
#
# 2020-02-27,19:17,BS,"",0,"","","","","",https://www.coronavirus.bs.ch/nm/2020-coronavirus-erster-positiver-fall-in-basel-stadt-zweiter-positiv-getesteter-ausserkantonaler-fall-gd.html
# 
# example of an output row after the merge with this script
# 2020-02-27,19:17,'BS',0,0,0,0,0,0,0,https://www.coronavirus.bs.ch/nm/2020-coronavirus-erster-positiver-fall-in-basel-stadt-zweiter-positiv-getesteter-ausserkantonaler-fall-gd.html,,
#
# this simple script may be improved ;-) 
#

import csv, os, glob

#
# Change the following to adapt to your env
#
inp_path = '../fallzahlen_kanton_total_csv'
out_path = '../'
tmp_merge = out_path + 'tmp_CH_merge.csv'
# tmp_sort = out_path + 'tmp_CH_sort.csv'
CH_komplett = out_path + 'CH_daten.csv'

# at the end put this line at the top of the sorted file
# Die letzten beiden Spalten sind nicht konsequent richtig gefuellt. Die Daten in den Kanton-Files unterscheiden sich hier.
#header_row = 'date,time,abbreviation_canton_and_fl,ncumul_tested,ncumul_conf,ncumul_hosp,ncumul_ICU,ncumul_vent,ncumul_released,ncumul_deceased,source,TotalPosTests1,TotalCured\n'
header_row = 'date,time,abbreviation_canton_and_fl,ncumul_tested,ncumul_conf,ncumul_hosp,ncumul_ICU,ncumul_vent,ncumul_released,ncumul_deceased,source\n'

# ---
# Merge all cantons & FL files
# ---
merged_files = open(tmp_merge, 'w')
for filename in glob.glob(os.path.join(inp_path, '*.csv')):
        file = open (filename, 'r')
        # skip first row
        rows = file.readlines()[1:] 
        for line in rows:
           new_line = line.replace("\"\"","")
           merged_files.write(new_line)
merged_files.close()

# ---
# Sort merged_files by date,time...
# ---
ch_file = open(CH_komplett, 'w')
ch_file.write(header_row)
tmp_ch = open(tmp_merge, 'r')

reader = csv.reader(tmp_ch,  delimiter=",")

# sort order by [0] date, [2] kanton
sortedlist = sorted(reader, key=lambda row:(row[0], row[2]), reverse=False)

for lines in sortedlist:
  row = ','.join([str(item) for item in lines ])
  
  # zerlege row und fill in default values
  arr = row.split(",")
  
  # time set to 00:00 if emtpy
  if not arr[1]:
      arr[1] = "00:00"
  
  # Kantonsbezeichnung sind Strings 
  arr[2] = "'" + arr[2] + "'"

  # von [3] bis [9] sind alles Integer
  # Default ist 0
  idx = [3,4,5,6,7,8,9]
  for i in idx: 
    if not arr[i]:
      arr[i] = 0
      #print (arr[i])
  
  # source ist ein String
  arr[10] = "'"+arr[10]+"'"

  # Felder [11] und [12] werden nicht validiert

  new_cs_row = ','.join(map(str, arr))
  ch_file.write(new_cs_row+"\n")
   
#
# 
#
