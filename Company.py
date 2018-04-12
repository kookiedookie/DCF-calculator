"""
This is the Company class file. Each Company object has 2 attributes:
    stockticker <type: string> and data <type: dictionary>.

Created 23 March 2018

@authors:
    Ng Hao Wei (haowei.ng.2014)
    Dylan Chan (dylan.chan.2016)
    Nurul Suhailah Binte Sapnan (suhailahs.2015)
"""

#import packages
import pandas as pd
#import pandas_datareader.data as pdr
import numpy
from dateutil.relativedelta import relativedelta
from datetime import datetime
import quandl

    #%%
    #Local Functions
def strtofloat(aList):
    """ Converts string elements in list to float """
    x = []
    try:
        x = list(map(float,aList))
    except ValueError:
        print("Error! Check if financial data is available. Common" +
              " culprits: interest expense, tax expense.")
        raise
    return x

def factor_correction(values):
    """ Multiplies values by 1000 """
    return(list(x*1000 for x in values))

def arrayRatio(numerator,denominator):
    """
    Returns the average ratio of numerator to denominator.
    E.g. Given numerator ['123','456'] and denominator ['222','333'],
    returns 1.043...
    """
    lennum = len(numerator)
    lenden = len(denominator)
    lenlower = min(lennum,lenden) #finds list with less values
    eachRatio = list()
    for i in range(lenlower):
        #finds ratio for each year and appends to eachRatio
        eachRatio.append(numerator[i]/denominator[i])
    averageRatio = sum(eachRatio)/len(eachRatio) #averages the ratios
    return averageRatio



#%%
#Online data pull function
def onlinedata(stockticker, apikey):
    """
    Returns all financial data from all sources in the form of dictionary

    Refer to the return statement for keys and values
    """
#%%
        #Source 1: yahoo finance
    yahoo_URL = 'https://sg.finance.yahoo.com/quote/'

            #yahoo summary
    yahoo_summary_param = '?p='
    yahoo_summary_URL = (yahoo_URL + 
                         stockticker + 
                         yahoo_summary_param + 
                         stockticker)

                #market cap
    summary_marketcap_dataframe = pd.read_html(yahoo_summary_URL,
                                               match='Market cap',
                                               index_col=0)
    marketcap = summary_marketcap_dataframe[0].loc['Market cap',1]

    if marketcap[-1] == 'K':
        marketcap = marketcap[:-1]
        marketcap = float(marketcap) * 1_000
    elif marketcap[-1] == 'M':
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

            #previous close price
    summary_prevclose_dataframe = pd.read_html(yahoo_summary_URL,
                                               match='Previous close',
                                               index_col=0)
    current_price = float(
            summary_prevclose_dataframe[0].loc['Previous close',1])
    #previous close is proxy for current stock price

            #yahoo key stats
    yahoo_keystats_param = '/key-statistics?p='
    yahoo_keystats_URL = (yahoo_URL + 
                          stockticker + 
                          yahoo_keystats_param +
                          stockticker)

                #beta
    keystats_beta_dataframe = pd.read_html(yahoo_keystats_URL,
                                           match='Beta',
                                           index_col=0)
    
    beta = float(keystats_beta_dataframe[0].loc['Beta',1]) #beta

                #Number of shares outstanding
    keystats_numshares_dataframe = pd.read_html(yahoo_keystats_URL,
                                                match='Shares outstanding',
                                                index_col=0)
    numshares = keystats_numshares_dataframe[0].loc['Shares outstanding 5',1]
    if numshares[-1] == 'K':
        numshares = numshares[:-1]
        numshares = float(numshares) * 1_000
    elif numshares[-1] == 'M':
        numshares = numshares[:-1]
        numshares = float(numshares) * 1_000_000
    elif numshares[-1] == 'B':
        numshares = numshares[:-1]
        numshares = float(numshares) * 1_000_000_000
    elif numshares[-1] == 'T':
        numshares = numshares[:-1]
        numshares = float(numshares) * 1_000_000_000_000
    else:
        numshares = float(numshares)


            #yahoo income statement
    yahoo_financials_param = '/financials?p='
    yahoo_financials_URL = (yahoo_URL + 
                            stockticker + 
                            yahoo_financials_param +
                            stockticker)
    incstmt = pd.read_html(yahoo_financials_URL,index_col=0)

                #interest expense, tax expense, and income before tax

    intexp = factor_correction(
                strtofloat(
                    incstmt[0].loc['Interest expense'].values.tolist()))
    #interest expense over last 3 years
    taxexp = factor_correction(
                strtofloat(
                    incstmt[0].loc['Income tax expense'].values.tolist()))
    #tax expense over last 3 years

    ebt = factor_correction(
                strtofloat(
                    incstmt[0].loc['Income before tax'].values.tolist()))
    #income before tax over last 3 years
    ebit = factor_correction(
                strtofloat(
                    incstmt[0].loc[
                    'Earnings before interest and taxes'].values.tolist()))
    # ebit as a float over the past 3 years taken from
    #   Yahoo Finance and multiplied by 1000
    lastebit = ebit[0]

            #yahoo balance sheet
    yahoo_balsht_param = '/balance-sheet?p='
    yahoo_balsht_URL = (yahoo_URL + 
                        stockticker + 
                        yahoo_balsht_param + 
                        stockticker)
    balsht = pd.read_html(yahoo_balsht_URL,index_col=0)

                #debt
    TD = factor_correction(
            strtofloat(
                    balsht[0].loc['Total liabilities'].values.tolist()))
    #total debt over last 3 years
    CD = factor_correction(
            strtofloat(
                    balsht[0].loc[
                            'Total current liabilities'].values.tolist()))
    #current debt over last 3 years
    LTD = [td - cd for td,cd in zip(TD,CD)]
    #long-term debt over last 3 years
    lastD = LTD[0]
    #long term debt of latest year

                #working capital
                    #change in current assets
    current_assets = factor_correction(
                        strtofloat(
                            balsht[0].loc[
                                    'Total current assets'].values.tolist()))
    ybca = current_assets[1] #Year Begining Current Assets
    yeca = current_assets[0] #Year Ending Current Assets

                    #change in current liabilities
    current_liabilities = factor_correction(
                            strtofloat(
                                balsht[0].loc[
                                'Total current liabilities'].values.tolist()))
    ybcl = current_liabilities[1] #Year Beginning Current Liabilities
    yecl = current_liabilities[0] #Year Ending Current Liabilities

        #yahoo cash flow
    yahoo_cashflow_param = '/cash-flow?p='
    yahoo_cashflow_URL = (yahoo_URL + 
                          stockticker + 
                          yahoo_cashflow_param + 
                          stockticker)
    cashflow = pd.read_html(yahoo_cashflow_URL,index_col=0)

            #Depreciation, Capital Expenditure and Amortisation
    if cashflow[0].loc['Depreciation'].values.tolist()[0] == '-':
        dep = 0
    else:
        dep = factor_correction(
                strtofloat(
                    cashflow[0].loc[
                            'Depreciation'].values.tolist()))[0]

    if cashflow[0].loc['Capital expenditure'].values.tolist()[0] == '-':
        capex = 0
    else:
        capex = factor_correction(
                    strtofloat(
                        cashflow[0].loc[
                            'Capital expenditure'].values.tolist()))[0]
    #most recent capex value

    if balsht[0].loc['Accumulated amortisation'].values.tolist()[0] == '-' :
        #test if amor is NIL/'-'
        amor = 0 #if yes, set amor to 0, because no amortisation
    else:
        #else, take amor value from balance sheet
        amor = factor_correction(
                    strtofloat(balsht[0].loc[
                        'Accumulated amortisation'].values.tolist()))[0]
    #amortisation value from Yahoo finance of the past 3 years,
    #set amor used to the most recent year

        #%%
        #yahoo historical prices
            #standard deviation of adj close prices
    todaydate = datetime.today()
    yearsagodate = todaydate - relativedelta(years=5)
    today = todaydate.strftime('%Y-%m-%d')
    yearsago = yearsagodate.strftime('%Y-%m-%d')
    p =[]
    count = 0
    while True:
        try:
            p = numpy.array(
                    quandl.get(
                            ('WIKI/' + stockticker),
                            start_date = yearsago,
                            end_date = today,
                            collapse='monthly',
                            api_key = apikey
                            )['Close'].tolist())
            break
        except:
            print("Error occurred on while loop line ~260!" + 
                  " Trying again")
            count += 1
            if count >8:
                print("Tried 10 times on line ~260. Stopped.")
            
            
    p = p[~numpy.isnan(p)]
    stdev = numpy.std(p)

    #%%
            #Expected market returns: compound annual growth rate of monthly
            #SP500 adj close prices over 5 years
    rmt = []
    count = 0
    while True:
        try:
            rmt = numpy.array(
                    quandl.get(
                            'ECB/FM_Q_US_USD_DS_EI_S_PCOMP_HSTA',
                            start_date = yearsago,
                            end_date = today,
                            api_key = apikey
                            )['Points'].tolist())
            break
        except:
            print("Error occurred on while loop line ~285!" +
                  " Trying again")
            count += 1
            if count >8:
                print("Tried 10 times on line ~285. Stopped.")            
            
    rmt = rmt[~numpy.isnan(rmt)]
    rm = numpy.average(numpy.diff(rmt)/rmt[:-1])*4 
    #convert quarterly growth rate to CAGR
    #%%

    #Source 2: 3 month T-bills -- https://www.federalreserve.gov/releases/h15/
    fedreserve_URL = 'https://www.federalreserve.gov/releases/h15/'
    fedint_dataframe = pd.read_html(fedreserve_URL)
    fedint_row = fedint_dataframe[0].loc[15].values.tolist()
    #retreives row 15 (3-month T-bils)
    del fedint_row[0] #removes first value i.e. '3-month'
    rf = (sum(strtofloat(fedint_row))/len(fedint_row))/100
    #risk free rate (3m T-Bills)


    return {'marketcap':marketcap,
            'current_price':current_price,
            'beta':beta,
            'numshares':numshares,
            'intexp':intexp,
            'taxexp':taxexp,
            'ebt':ebt,
            'lastebit':lastebit,
            'ybca':ybca,
            'yeca':yeca,
            'ybcl':ybcl,
            'yecl':yecl,
            'TD':TD,
            'CD':CD,
            'LTD':LTD,
            'lastD':lastD,
            'dep':dep,
            'capex':capex,
            'amor':amor,
            'stdev':stdev,
            'rf':rf,
            'rm':rm
            }

 #%%
class Company:
    def __init__(self,stockticker,apikey):
        self.stockticker = stockticker
        self.apikey = apikey
        self.data = onlinedata(stockticker, apikey)