import csv
import urllib.request
from bs4 import BeautifulSoup
import ftplib
import time
import datetime
import os

###################################
### Download CSV file from URL. ###
###################################

url = 'http://sandbox.lbcc.linnlibraries.org/example_solr_export.csv'
response = urllib.request.urlopen(url)
text =  response.read().decode('utf-8')

soup = BeautifulSoup(text, 'html.parser')
cr = csv.reader(soup.pre.get_text().split("\n"), delimiter=',', quotechar='"')

#######################################
# Extract ISBN info (from 5th column) #
#######################################

ISBN_postsort = []

for row in cr:
    if len(row) >1:
        if row[5] != "":
            ISBN_postsort.append(row[5])

######################################################
# Format: singleISBN is a list ['isbn','isbn2' ....] #
######################################################

isbnList = []

data = ISBN_postsort

singleISBN = []

for i in range(len(data)):
    testISBN = data[i].split(',')
    if len(testISBN) >1:
        for i in range(len(testISBN)):
            singleISBN.append(testISBN[i])
            
############################################################
#Format: testISBN is a sequence [['isbn1'], ['isbn2'] ... ]#
############################################################
            
testISBN = []

for i in range(len(singleISBN)):
    mListISBN = [singleISBN[i]]
    testISBN.append(mListISBN)

for i in range(len(data)):
    splitISBN = data[i].split(",")

#########################
# Format: Insert header #
#########################

testISBN.insert(0, ['ISBN'])

####################################################
### Create timestamp and title for new CSV file. ###
####################################################
    
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')

csvname = 'LINzz.' + st + '.xls'

###############################################
### Create new CSV file with list of ISBNs. ###
###############################################

with open(csvname,'w') as fp:
    a = csv.writer(fp,delimiter=',', lineterminator='\n')
    data = testISBN
    a.writerows(data)

##########################################
### Upload new CSV file to FTP server. ###
##########################################
    
s = ftplib.FTP('IP','USERNAME','PASSWORD')
ftppath = '/FILEPATH'
s.cwd(ftppath)
f = open(csvname,'rb')                
s.storbinary('STOR ' + csvname, f)         

f.close()                                
s.quit()

#############################################
### Delete CSV file from local directory. ###
#############################################

os.remove(csvname)


