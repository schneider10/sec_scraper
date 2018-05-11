# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 19:39:24 2018

SEC XML parser

Goals: Intake CIK codes and gather all xbrl filings for these codes.
    -Historic data
        -use monthly rss feeds url to cycle through all historic data. If match is found with CIK code, 
        store filing in the folder for that CIK code.
        -Does Jim want all historic data stored or only those that pertain to these CIK codes?
    -Recent data
    
    -Use class structure to make properly
"""


import urllib2
import xml.etree.ElementTree as ET
#import zipfile
import os
#from StringIO import StringIO


#Function to convert url to string

def read_url(selected_url):
    response = urllib2.urlopen(selected_url)
    url_as_string = response.read()
    response.close()
    return url_as_string
    
# Function to parse xml into CIK codes and associated Zip files, returning a list of each.
    
def parse_xml(xbrl_url):
    rss_xml = read_url(xbrl_url)
    # Use elemenet tree module to parse XML and extract Zip URLs and CIK codes

    root = ET.fromstring(rss_xml)
    edgar = '{http://www.sec.gov/Archives/edgar}'
    cik_list = []
    zip_list = []
    
    # Grabs all Zip URLs in RSS feed
    for zip_files in root.iter('enclosure'):
        zip_list.append(zip_files.attrib['url'])
    # Grabs all CIK codes in RSS feed
    for cik_codes in root.iter(edgar + 'cikNumber'):
        cik_list.append(cik_codes.text)
    if len(cik_list) != len(zip_list):
        print "WARNING! Different number of CIK codes than .ZIP files"
    return (cik_list, zip_list)     
        

# Funciton to pull xbrl_filing zip files from SEC and dump them on PC

def insert_xbrl_files(month,year):
    month_list = ["Jan","Feb","Mar","Apr","May","June",
                  "July","Aug","Sept","Oct","Nov","Dec",
                 ]
                 
    year = str(year)
    
    if month < 10:
        month = '0' + str(month)
    else:
        month = str(month)
        
    # Check for year and month directorys in dump directory and build if not present 

    if not os.path.exists(dump_dir + '/' + year):
        os.makedirs(dump_dir + '/' + year)
 
    month_dump_dir = dump_dir + '/' + year + '/' + month_list[int(month) - 1]
    if not os.path.exists(month_dump_dir):
        os.makedirs(month_dump_dir)
    
    # Read XML from SEC xbrl archive url and parse out list of CIK codes and associated .zip files
    
    xbrl_url = ['http://www.sec.gov/Archives/edgar/monthly/xbrlrss-' 
                + year + '-' + month + '.xml'
               ]
                
    cik_list, zip_list = parse_xml(xbrl_url)
    
    # Grabs all zip files with matching CIK code to one in txt file.
    zip_count = 0
   
    for cik_code_index in range(len(zip_list)):
        
        # If CIK code is located in the set of selected CIK codes, grab its zip file.
        if cik_list[cik_code_index] in my_cik_codes:
            
            # Create directory for CIK code in Month and Year folder
            cik_dump_dir = month_dump_dir + '/' + cik_list[cik_code_index]
            if not os.path.exists(cik_dump_dir):
                os.makedirs(cik_dump_dir)
            
            # Select specific zip_file
            print "zip file for CIK code " + cik_list[cik_code_index] \
                  + " found"
            zip_file = zip_list[cik_code_index]
            print zip_file
            
            # Save specific zip_file to dump folder with name as SEC accession number
            last_slash_loc = zip_file.rfind('/') + 1
            output = open(cik_dump_dir + '/' + zip_file[last_slash_loc:], "w")
            read_zip = read_url(zip_file)
            output.write(read_zip)
            output.close()
            
            zip_count += 1
            
    print str(zip_count) + " zip files found"        
            
       

# Code begins here

# Ask where to dump directory and build it if not present ... warning message if it is.

askusr_dir = '/home/stephen/Desktop'
dump_dir = askusr_dir + '/SEC_dump'

if not os.path.exists(dump_dir):
    os.makedirs(dump_dir)
else:
    print "WARNING: dump directory is already present. Rewrite contents?"

# Makes a set of all cik codes... File is decoded to unicode to remove UTF-8 BOM

with open("CIK Codes.txt") as f:
    my_cik_codes_list = f.read().decode("utf-8-sig").encode("utf-8").splitlines()
    
my_cik_codes = set(my_cik_codes_list)

start_year = 2017
start_month = 12    
end_year = 2018
end_month = 1

year_diff = end_year - start_year
for year_index  in range(0,year_diff + 1):
    year = start_year + year_index
 
    # Months are first created from the start month to Dec (13)
    if year == start_year:    
        for month in range(start_month,13):        
            print month, year
            insert_xbrl_files(month,year)   
            
   # Months will then be created from Jan (1) to the end month.
    elif year == end_year:
        for month in range(1,end_month + 1):
            print month, year
            insert_xbrl_files(month,year)   
    else:
        for month  in range(1,13):
            print month, year
            insert_xbrl_files(month,year)            











# condition if only year is selected
# prevent selection of only a month
        
'''    
read_zip = read_url(zip_list[0])
zipdata = StringIO()
zipdata.write(read_zip)

#Pull out files from a zip file
zip_ref = zipfile.ZipFile(zipdata)
#Put these internal files into a specific directory on local pc (or cloud)
zip_ref.extractall('/home/stephen/Desktop')
zip_ref.close()
'''

# Recent Data
'''


#Starting URL

RSS_URL = 'https://www.sec.gov/Archives/edgar/xbrlrss.all.xml'

#Read URL
rss_xml = read_url(RSS_URL)
#Read XML as string and parses into elements
root = ET.fromstring(RSS_XML)
edgar = '{http://www.sec.gov/Archives/edgar}'
cik_list = []
filing_dates = []
for items in root.iter(edgar + 'filingDate'):
    filing_dates.append(items)
   
for items in root.iter(edgar + 'cikNumber'):
    cik_list.append(items)
    print items.text

url_list = []
url_description = []
for items in root.iter(edgar + 'xbrlFile'):
    
    descriptions =  items.attrib[edgar +'description']
    urls = items.attrib[edgar + 'url']
    url_description.append(descriptions)    
    url_list.append(urls)

xbrl_response = urllib2.urlopen(url_list[5])
xbrl_read = xbrl_response.read()
xbrl_response.close()

'''