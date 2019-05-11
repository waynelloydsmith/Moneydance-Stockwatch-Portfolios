#!/usr/bin/env python
# called by updatePortfolioStockwatch.py
import sys
import urllib2
import urllib
#import org.sqlite
from java.lang import Class
from java.sql import DriverManager , SQLException

##### sqlite is broken in MD 2019 so had to use another JVM to get the stockwatch ID from seamonkey 
import sys
import urllib2
import urllib
import subprocess

# use jython to get the cookie . sqlite is broken in moneydance 2019
try:
            output = subprocess.check_output(
                ['jython', '/opt/moneydance/scripts/fetch-Stockwatch-ID.py'],
                stderr=subprocess.STDOUT).decode('UTF-8')
#	        universal_newlines=True).decode('UTF-8')
except subprocess.CalledProcessError as e:
            print "It Failed"
            print e.output  # Traceback messages 
            raise
	  
print "output=",output # normal print from python script
            
file1 = open('/opt/moneydance/scripts/tmp/stockwatchID.txt', 'rb')
print file1    
XXX = file1.read()
file1.close()
print XXX




file2 = open('/opt/moneydance/scripts/tmp/StockwatchPortfolio/stockwatch.csv', 'wb') # where we will put the data 
print file2


##Class.forName("org.sqlite.JDBC").newInstance()
# now to get the XXX cookie value that seamonkey is using
##dbConn = DriverManager.getConnection("jdbc:sqlite:/home/wayne/.mozilla/seamonkey/i0tpuie4.default/cookies.sqlite")
##stmt = dbConn.createStatement()
##resultSet = stmt.executeQuery("select * from moz_cookies where baseDomain == 'stockwatch.com' AND name == 'XXX'")
##XXX =  resultSet.getString(5)



#url =  'https://www.stockwatch.com/Quote/Download.aspx?type=date&format=ascii&dest=file&date=20171222&exopt=N&ex=T&ats=N&id=userID&pw=password' # end of day closing worked great
#url = 'https://www.stockwatch.com/Quote/WebQuery.aspx?what=quote&format=comma&fields=SXRLVOHITE&pf=1&region=C&header=Y' # my portfolio failed 
#url = 'https://www.stockwatch.com/Quote/WebQuery.aspx?what=quote&format=comma&fields=SXRLVOHITE&pf=1&region=C&header=Y&id=userID&pw=password' # my portfolio worked great
url = 'https://www.stockwatch.com/Quote/WebQuery.aspx?what=quote&format=comma&fields=SXRLVOHITE&pf=1&region=C&header=Y' # works
#url = 'https://www.stockwatch.com/Quote/Download.aspx?type=date&format=ascii&dest=file&exopt=N&ex=T&ats=N&id=userID&pw=password' # most recent end of day closing no date returns empty file if markets are closed
print url
opener = urllib2.build_opener()
#opener.addheaders = [('User-Agent', 'Mozilla/5.0')] # was enough to fool NEO 
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0 SeaMonkey/2.49.1 Slackware/14.2')]
opener.addheaders.append(('Cookie','XXX='+XXX)) # success
# could have used the &auth=XXX paramter for WebQuery.aspx but the above works with Download.aspx too


req = urllib2.Request(url)
try:
#  response = urllib2.urlopen(req)
  response = opener.open(url)
except urllib2.URLError as e:
    if hasattr(e, 'reason'):
        print 'We failed to reach a server.'
        print 'Reason: ', e.reason
    if hasattr(e, 'code'):
        print 'The server couldn\'t fulfill the request.'
        print 'Error code: ', e.code
else:  
  print response.headers   
  webContent = response.read()          
  print 'length=', len(webContent)       
  print webContent


  file2.write(webContent) # this function does not return anything useful .. I changed the permission on the file and crashed the program with an IOError:[Errno 13] Permission denied:  
  file2.close()  # so f.close is not the same as f.close()
  execfile("updatePortfolioStockwatch2Moneydance.py") # process the csv file
  print "Done updatePortfolio1Stockwatch.py"