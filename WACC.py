# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 15:19:05 2018

@author: Sherman

Returns the Weighted Average Cost of Capital (WACC) using data from Yahoo Finance

Input -- stockticker (e.g. 'AMZN')
Output -- WACC (e.g. 0.4)
"""

#Import Packages and Modules ------------------------------------------------------------------------------------
import pandas as pd

#Local Functions ------------------------------------------------------------------------------------
def strtofloat(aList):
    """ Converts string elements in list to float """
    return list(map(float,aList))


def arrayRatio(numerator,denominator):
    """ Returns the average ratio of numerator to denominator. 
    
    Keyword arguments:
        numerator -- array of 'float' elements (e.g. interest expenses over 3 years)
        denominator -- array of 'float' elements (e.g. total debt over 3 years)
    Output:
        averageRatio -- float (e.g. average cost of debt over 3 years)
    """
    lennum = len(numerator)
    lenden = len(denominator)
    lenlower = min(lennum,lenden) #finds list with less values (ISSUE: what if year 2 missing?)
    eachRatio = list()
    for i in range(lenlower): #finds ratio for each year and appends to eachRatio
        eachRatio.append(numerator[i]/denominator[i])
    averageRatio = sum(eachRatio)/len(eachRatio) #averages the ratios
    return averageRatio
    
def gmean(lst):
    """ Returns geometric mean of list of values. """
    gmean = 1
    for i in lst:
        gmean *= (1+(i/100))
    return gmean**(1/len(lst))-1


#Inputs ------------------------------------------------------------------------------------
stockticker = 'AMZN' #stock ticker symbol from input

#Data Collection ------------------------------------------------------------------------------------
    #Source 1: yahoo finance
yahoo_URL = 'https://sg.finance.yahoo.com/quote/'



        #yahoo summary
yahoo_summary_param = '?p='
yahoo_summary_URL = yahoo_URL + stockticker + yahoo_summary_param + stockticker

            #market cap
summary_marketcap_table = pd.read_html(yahoo_summary_URL,match='Market cap', index_col=0)
marketcap = summary_marketcap_table[0].loc['Market cap',1]
if marketcap[-1] == 'M':
    marketcap = marketcap[:-1]
    marketcap = float(marketcap) * 1_000_000
elif marketcap[-1] == 'B':
    marketcap = marketcap[:-1]
    marketcap = float(marketcap) * 1_000_000_000
elif marketcap[-1] == 'T':
    marketcap = marketcap[:-1]
    marketcap = float(marketcap) * 1_000_000_000_000
else:
    marketcap = float(marketcap)



        #yahoo key stats
yahoo_keystats_param = '/key-statistics?p='
yahoo_keystats_URL = yahoo_URL + stockticker + yahoo_keystats_param + stockticker

            #beta
keystats_beta_table = pd.read_html(yahoo_keystats_URL,match='Beta',index_col=0)
beta = float(keystats_beta_table[0].loc['Beta',1]) #beta



        #yahoo income statement
yahoo_financials_param = '/financials?p='
yahoo_financials_URL = yahoo_URL + stockticker + yahoo_financials_param + stockticker
incstmt = pd.read_html(yahoo_financials_URL,index_col=0)

            #interest expense, tax expense, and income before tax
intexp = strtofloat(incstmt[0].loc['Interest expense'].values.tolist()) #interest expense over last 3 years
taxexp = strtofloat(incstmt[0].loc['Income tax expense'].values.tolist()) #tax expense over last 3 years
EBT = strtofloat(incstmt[0].loc['Income before tax'].values.tolist()) #income before tax over last 3 years



        #yahoo balance sheet
yahoo_balsht_param = '/balance-sheet?p='
yahoo_balsht_URL = yahoo_URL + stockticker + yahoo_balsht_param + stockticker
balsht = pd.read_html(yahoo_balsht_URL,index_col=0)

            #debt
TD = strtofloat(balsht[0].loc['Total liabilities'].values.tolist()) #total debt over last 3 years
CD = strtofloat(balsht[0].loc['Total current liabilities'].values.tolist()) #current debt over last 3 years
LTD = [td - cd for td,cd in zip(TD,CD)] #long-term debt over last 3 years
lastD = LTD[0] #long term debt of latest year




    #Source 2: 3 month T-bills -- https://www.federalreserve.gov/releases/h15/
fedreserve_URL = 'https://www.federalreserve.gov/releases/h15/'
fedint_table = pd.read_html(fedreserve_URL)
fedint_row = fedint_table[0].loc[15].values.tolist() #retreives row 15 (3-month T-bils)
del fedint_row[0] #removes first value i.e. '3-month'
rf = (sum(strtofloat(fedint_row))/len(fedint_row))/100 #risk free rate (3m T-Bills)



    #Source 3: SP500 annual returns - https://ycharts.com/indicators/sandp_500_total_return_annual
ycharts_URL = 'https://ycharts.com/indicators/sandp_500_total_return_annual'
ycharts_table = pd.read_html(ycharts_URL)
ycharts_5years = ycharts_table[0][1][2:8].values.tolist() #retreives last 5 years SP500 returns
phlist = []
for i in ycharts_5years: #removes '%' from last char in each string element
    i = i[:-1]
    phlist.append(i)
phlist = strtofloat(phlist)
rm = gmean(phlist) #expected market rate -- annualised average of 5 years annual returns from SP500



#calculations
rp = rm-rf #market risk premium
re = rf + beta*rp #cost of equity
rd = arrayRatio(intexp,LTD) #cost of debt
V = lastD + marketcap # long term debt + market capitalisation
taxrate = arrayRatio(taxexp,EBT) #average tax rate
Dr = lastD/V #debt ratio at latest year
Er = marketcap/V #equity ratio at latest year
DEr = lastD/marketcap #debt to equity ratio

WACC = Er*re + (Dr*rd*(1-taxrate)) #applies WACC formula

print ("WACC is " + str(WACC)) #prints WACC if it works