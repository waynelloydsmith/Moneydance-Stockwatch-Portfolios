#!/usr/bin/env python
#called by  fetchDaylyStockwatch.py and fetchDaylyStockwatchIndex.py 
import sys
from java.sql import DriverManager , SQLException
###
#import org.sqlite.JDBC # was just import org.sqlite and it worked with java 161 but not with 144
import org.sqlite

# now to get the XXX cookie value that seamonkey is using to login to Stockwatch
###
dbConn = DriverManager.getConnection("jdbc:sqlite:/home/wayne/.mozilla/seamonkey/i0tpuie4.default/cookies.sqlite")
###
stmt = dbConn.createStatement()
###
resultSet = stmt.executeQuery("select * from moz_cookies where baseDomain == 'stockwatch.com' AND name == 'XXX'")
###
XXX =  resultSet.getString(5) # raises java.SQLException:ResultSet closed if Stockwatch is not logged in.
print XXX
###       44000922%2c385549%2c636905%2cuserName
file2 = open('/opt/moneydance/scripts/tmp/stockwatchID.txt', 'wb')
print file2
file2.write(XXX) # for some reason this ends up being returned to the caller too.
file2.close() 
print "Done fetch-Stockwatch-ID.py"
