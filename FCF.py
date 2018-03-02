#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 11:13:34 2018


@author: Dylan
"""


import pandas as pd
#define common functions 
def avg_tax_rate(income_tax_expense, income_before_tax):
    """Returns average tax rate of the tax_expense over taxable income


    Keyword arguments:
        income _tax_expense - list of ‘float’ elements (tax expense over the past 3 years)
        income_before_tax - list of ‘float’ elements (taxable income over the past 3 years) 


    Output:
        avg_tax_rate -  float (avg tax rate) 
    """




    lente  = len(income_tax_expense)
    lenti = len(income_before_tax)
    lenlower = min([lente,lenti]) #finds list with less values (ISSUE: what if year 2 missing?)
    yearlytaxrate = list()
    for i in range(lenlower): #finds taxrate for each year and appends to yearly tax rate
                  yearlytaxrate.append((income_tax_expense[i])/(income_before_tax[i]))
                  avg_tax_rate = sum(yearlytaxrate)/len(yearlytaxrate) #averages the yearly tax rates 
    return avg_tax_rate


def strtofloat(aList):
    """ Converts string elements in list to float """
    return list(map(float,aList))




#stores input(s) into variable
stockticker = 'AMZN' #stock ticker symbol from input


#collects data from yahoo finance [ISSUE: not changing with stockticker yet]
incstmt = pd.read_html('https://sg.finance.yahoo.com/quote/AMZN/financials?p=AMZN',index_col=0)
#incomestatement


balsht = pd.read_html('https://sg.finance.yahoo.com/quote/AMZN/balance-sheet?p=AMZN',index_col=0)


cashflow = pd.read_html('https://sg.finance.yahoo.com/quote/AMZN/cash-flow?p=AMZN', index_col=0)
#cashflow 


income_tax_expense = incstmt[0].loc['Income tax expense'].values.tolist()
income_before_tax = incstmt[0].loc['Income before tax'].values.tolist()




# values required to pull out from yahoo finance
ebit = strtofloat(incstmt[0].loc['Earnings before interest and taxes'].values.tolist()) # ebit over the past 3 years    
ebit = ebit[0] #most recent EBIT value 


ite = strtofloat(incstmt[0].loc['Income tax expense'].values.tolist()) #Income tax expense past 3 years, type float
ibt = strtofloat(incstmt[0].loc['Income before tax'].values.tolist()) #Income before tax past 3 years, type float
atr = avg_tax_rate(ite, ibt) #average tax rate as a float 


dep = strtofloat(cashflow[0].loc['Depreciation'].values.tolist()) #depreciation of past 3 years 
dep = dep[0] #most recent depreciation 


capex = strtofloat(cashflow[0].loc['Capital expenditure'].values.tolist())
capex = capex[0] #most recent capex value 


current_assets = strtofloat(balsht[0].loc['Total current assets'].values.tolist())
ybca = current_assets[1] #year begining Current assets 
yeca = current_assets[0] #year ending Current assets 
cca = ybca - yeca #Change in Current assets, year beg - year end 
current_liabilities = strtofloat(balsht[0].loc['Total current liabilities'].values.tolist())
ybcl = current_liabilities[1]
yecl = current_liabilities[0]
ccl = yecl- ybcl # change in current liabilities, year end - year begining
cwc = cca + ccl #Change in working capital formula 


if balsht[0].loc['Accumulated amortisation'].values.tolist()[0] == '-' : #test if amor is really NIL/'-'
    amor = 0 #if yes, set amor to 0, because no amortisation 
else:
    amor = strtofloat(balsht[0].loc['Accumulated amortisation'].values.tolist()) #amortisation value from Yahoo finance (Amor here is '-' /NIL, therefore equate to 0,
# other variables might face this issue as well )
    amor = amor[0]
             
FCF = ebit*(1 - atr)+ dep + amor - cwc - capex #Free Cash Flow equation


r = #rate of growth of cash flow (decide which method to draw this value)