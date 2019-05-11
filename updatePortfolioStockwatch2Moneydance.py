# called by updatePortfolio1Stockwatch.py and updatePortfolio2Stockwatch.py after they create the csv files
import sys

# the import data files should be down loaded from www.stockwatch.com and be placed in the directory /opt/moneydance/scripts/tmp/StockwatchDay
# goto www.stockwatch.com and click on quotes->download quotes-> Date -> select Exchange -> select csv format -> submit
# you must have a stockwatch account and be logged in
# one file per Exchange . Will contain all of closing values for all of the securties on that exchange . file name can be anything that ends in .csv
# this program processes all the .csv files in this directory and moves them to /opt/moneydance/scripts/tmp/Done
# the /opt/moneydance/scripts/tmp part of the directory name is defined in the definitions.py script
# Tested on Tsx , New York and Canadian Mutual funds 
# The mutual fund symbols the stockwatch uses are different than what is used by most sites . 
# the StockwatchSymbols list in definitions.py must be filled in to convert the symbols 
# example 'TML202':'BIF*CDN',  my moneydance symbol is TML202 . Stockwatch uses BIF*CDN for this same fund.
# stock symbols are automaticly converted by this program from AAA.AA.A to AAA-AA-A-T or AAA-AA-A-N
# ie the stockwatch dots are converted to GlobeIvestor dashes and the exchange is tacked on the end -T is TSX -N is newyork
# <ticker>	<date>	   <exchange>	<open>	<high>	<low>	<close>	<change>	<vol>	<trades>
# BRN*GLO	20141117	F	10.9856	10.9856	10.9856	10.9856	 -0.01	          0	0
# the above is the standard ASCII csv format produced by Stockwatch
# 
# Exchange codes used by Stockwatch
# Code 	Region 	Exchange
# U 	US 	Special code that matches any US symbol
# C 	Canada 	Special code that matches any Canadian symbol
# Z 	US 	Composite feed including the New York and American exchanges -- confirmed GlobeInvestor uses -N
# Q 	US 	Nasdaq, OTCBB, Pink Sheets and Other OTC
# O 	US 	OPRA - US Options
# S 	US 	S&P indexes
# P 	US 	PBOT indexes
# B 	US 	CBOE indexes
# I 	US 	Non-exchange and other indexes such as Dow Jones, Russel, Longon Gold Fix
# T 	Canada 	TSX - Toronto Stock Exchange -- confirmed same as GlobeInvestor
# V 	Canada 	TSX Venture Exchange
# M 	Canada 	Montreal Exchange
# C 	Canada 	CSE
# F 	Canada 	Canadian Mutual Funds  -- confirmed

# on the jython270 console run ----->>>execfile("updateDaylyStockwatch.py")
# issue #1 stockwatch doesn't use fundserv fund numbers so we have to convert them . example BIP151 = BRN*GLO
# issue #2 stockwatch is missing the mutual fund GOC309

class updatePortfolioStockwatch2Moneydance:
   import glob
   import sys
   execfile("/opt/moneydance/scripts/definitions.py")
   
   def setPriceForSecurity(symbol, price2, dateint , volume2 , high2 , low2 ): # this version is the latest Dec 29 2017

     root = moneydance.getRootAccount()
  ##   currencies = root.getCurrencyTable() fix from roywsmith
     AcctBook = root.getBook() 
     currencies = AcctBook.getCurrencies()
     if price2 != 0:
       price2 = 1/price2
     else:
       print "Error Zero Price found Skipping it"
       return
     if low2 != 0:
       low2   = 1/low2
     else:
       low2 = price2
     if high2 != 0:
       high2  = 1/high2
     else:
       high2 = price2 
     security = currencies.getCurrencyByTickerSymbol(symbol) #returns a CurrencyType
     if not security:
       print "No security with symbol/name: %s"%(symbol)
       return
     if dateint:
       snapshot = security.setSnapshotInt(dateint, price2) # this returns a CurrencyType.Snapshot
       security.setUserRate(price2)
       snapshot.setDailyVolume (long(volume2) )
       snapshot.setUserRate ( price2 )
       snapshot.setUserDailyHigh ( high2 )
       snapshot.setUserDailyLow ( low2 )
       security.setSnapshotInt(dateint, price2).syncItem() # added this April 19 2019 for change in MD2019
     else:  
       print "No Date for symbol/name: %s"%(symbol)

#     print price2,volume2,high2,low2
     print "Successfully set price for %s"%(security)	    	      
  
   
#url = 'http://www.stockwatch.com/Quote/WebQuery.aspx?what=quote&format=comma&fields=SXRLVOHITE&pf=1&region=C&header=Y&id=userID&pw=password' # my portfolio	   
# below is a sample of what the above produces 10 fields
#symbol,ex,region,prlast,volume,propen,prhigh,prlow,trades,lasttrade
#AD,T,C,20.61,13657,20.71,20.71,20.59,101,20171229 09:54:31
#ALA,T,C,28.38,67562,28.55,28.55,28.34,293,20171229 09:57:37
#BME*TFP,F,C,9.9582,0,,,,0,20171227 00:00:00
   
   files = glob.glob(definitions.directory+'StockwatchPortfolio/*.csv') # open the directory to be processsed 
                                                                  # should be a file containing the current prices for all the stocks/mutualfunds in my portfolio
   
#   print files
   
   for fle in files:
    fin = open(fle,'r')
#      with open(fle) as fin:
#      fin = open(fle,'r')
#	sym = fin.readline() # disgard the first line its a header
#	print sym            # print the header              
#   fin = open(definitions.directory+'Stockwatch.csv','r') # could use a hard coded file location  /opt/moneydance/scripts/tmp
    print fle   
    sym = fin.readline() # disgard the first line its a header
    print sym            # print the header           

    while 1:
       sym = fin.readline()
       if len(sym) <= 0:
         break
#       sym = sym.replace(',',' ') # strip out all the comma s
     
       lst = sym.split(",") # chop it up into 10 fields    

#       print lst[0] #ticker
#       print lst[1] #exchange
#       print lst[2] #region
#       print lst[3] #prlast
#       print lst[4] #volume
#       print lst[5] #propen
#       print lst[6] #prhigh
#       print lst[7] #prlow
#       print lst[8] #trades
#       print lst[9] #lasttrade time
       if lst[1] == 'F': # check the exchange field
#          print 'Its a Mutual Fund' # so we need to look up the symbol
          tickerSym = None
          Description = lst[0] # stockwatch symbol
#        Description = Description[:10] #20 was too long try 10 characters
#        print "DESC=", Description
     
          for fundsym , fundname in definitions.StockwatchSymbols.items():  # use the list in definitions to look up the mutual fund ticker
#        print fundsym , fundname
#        print len(fundname)
	     if len(fundname) <= 0: break
	     if  fundname.count (Description) > 0:
#	     print "found it", fundsym ,fundname
	       tickerSym = fundsym
#	     print "found tickerSym=",tickerSym
	       break
          if tickerSym == None:	
#	     print "updateDaylyStockwatch.py Ticker symbol Look up failed ------------------------"
	     continue
       else : 
         tickerSym = lst[0] # need to add a -T to the end of it to match the Globeinvestor standard
         tickerSym = tickerSym.replace('.','-')  #  sym = sym.replace(')',' ')  Stockwatch uses dots but GlobeInvestor uses dashes
         if lst[1] == 'T':
             tickerSym = tickerSym+'-T' # if its the TSX
         elif lst[1] == 'Z':    
             tickerSym = tickerSym+'-N' # if its the NewYork  Stockwatch and GlobeInvestor differ here  
         elif lst[1] == 'V':    
             tickerSym = tickerSym+'-X' # Toronto Venture Exchange Stockwatch and GlobeInvestor differ here      
         elif lst[1] == 'E':    
             tickerSym = tickerSym+'-NEO' # NEO Exchange         
         else:
	     print "Unknown Exchange ",lst[1]
	     raise ValueError('Unknown Exchange Code') # worked great execution stopped cold here
#	     x = 1/0  # this should crash the program worked got "ZeroDivisionError: integer division or modulo by zero"
#	     sys.exit("Unknown Exchange") # this killed moneydance ......... don't use it
       if len(lst[4]) > 0:	    
          volume = long (lst[4])
       else:
	  volume = 0
       if len(lst[6]) > 0:	    
          high = float ( lst[6] )
       else:
	  high = 0.0
       if len(lst[7]) > 0:	    
          low =  float  ( lst[7])
       else:
	  low = 0.0 
       
# --------------- looks like the date is already in the right format 20171229 09:57:37
       lst2 = lst[9].split() # chop it up into date and time     
       number = int( lst2[0] ) # this is the date
       print tickerSym,float(lst[3]),number,volume,high,low
       setPriceForSecurity(tickerSym,float(lst[3]),number , volume , high , low )            # this is a local function
###       print tickerSym,float(lst[6]),number,volume,high,low
#     break 
#   print fle+" time to move it"  # fle has a full path
    dest = fle
    dest = dest.replace('/',' ')
    dest = dest.strip()
    lst = dest.split()
    filename = lst[len(lst)-1]
#   print filename
    import os
    print definitions.directory+'Done/'+filename
    os.rename(fle, definitions.directory+'Done/'+filename) # /opt/moneydance/scripts/tmp/StockwatchPortfolio/stockwatch.csv
     
   print "Done updatePortfolioStockwatch2Moneydance.py"

