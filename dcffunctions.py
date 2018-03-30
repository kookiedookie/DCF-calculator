"""
This file contains the functions to calculate the DCF valuation and the 
intermediate results.

Created 23 March 2018

@authors:
    Ng Hao Wei (haowei.ng.2014)
    Dylan Chan (dylan.chan.2016)
    Nurul Suhailah Binte Sapnan (suhailahs.2015)
"""

#%%
#Local Functions

def arrayRatio(numerator,denominator):
    """ 
    Returns the average ratio of numerator to denominator. (e.g. Given 
    numerator ['123','456'] and denominator ['222','333'], returns 1.043...)
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
#Functions

def avg_tax_rate(income_tax_expenses_list, earnings_before_tax_list):
    """
    Returns average tax rate of the tax_expense over taxable income.
    """
    lente  = len(income_tax_expenses_list)
    lenti = len(earnings_before_tax_list)
    lenlower = min([lente,lenti]) #finds list with less values

    yearlytaxrate = list()
    for i in range(lenlower): 
        #finds taxrate for each year and appends to yearly tax rate
        yearlytaxrate.append(
                (income_tax_expenses_list[i]
                )/(
                earnings_before_tax_list[i]))
        avg_tax_rate = sum(yearlytaxrate)/len(yearlytaxrate) 
        #averages the yearly tax rates
    return avg_tax_rate

#%%
def cwc(caBeg,caEnd,clBeg,clEnd):
    """Returns change in working capital."""
    wcBeg = caBeg - clBeg
    wcEnd = caEnd - clEnd

    return wcEnd - wcBeg


#%%
def fcf(lastebit,atr,dep,amor,cwc,capex):
    """Returns free cash flow."""
    return lastebit*(1 - atr)+ dep + amor - cwc - capex

#%%
def five_year_fcf(FCF,growth_rate = 0.25):
    """
    Returns 5 year cashflow projection in a list of float
    elements calculated from estimated short term growth rate and free 
    cash flow.
    """
    #make it into dictionary
    year_0 = FCF
    year_1 = year_0*(1+growth_rate)
    year_2 = year_1*(1+growth_rate)
    year_3 = year_2*(1+growth_rate)
    year_4 = year_3*(1+growth_rate)
    year_5 = year_4*(1+growth_rate)

    return year_0,year_1,year_2,year_3,year_4,year_5

#%%
def re(rm,rf,beta):
    """Returns cost of equity using CAPM formula."""
    return rf + beta*(rm-rf)

#%%
def rd(intexp,LTD):
    """
    Returns cost of debt. Parameters are in list of float elements format.
    """
    return arrayRatio(intexp,LTD)

#%%
def wacc(marketcap,lastD,atr,re,rd):
    """Returns weighted average cost of capital."""
    V = marketcap+lastD
    Dr = lastD/V
    Er = marketcap/V
    return Er*re + (Dr*rd*(1-atr))
#%%
def tv(five_year_fcf, wacc, g= 0.03):
    """Returns terminal value using Gordon Growth formula."""
    last_fcf = five_year_fcf[-1]
    return last_fcf*(1+g) / (wacc - g)
#%%
def dcf(five_year_fcf,wacc,tv):
    """
    Returns expected present value of company based on discounted 
    cash flows valuation model.
    """
    total_years = len(five_year_fcf)-1
    pv = 0
    year = 0
    for fcf in five_year_fcf:
        pv += fcf/((1+wacc)**year)
        if year == total_years:
            pv += tv/((1+wacc)**(total_years))
        year+=1
    return pv

#%%
def target_price(dcf,lastD,numshares):
    return (dcf-lastD)/numshares

#%%
def recommendation(current_price,stdev,target_price):
    """
    Compares target price to current price, and 
    returns sell/hold/buy recommendation based on number of 
    standard deviations away from the mean.
    """
    distance = round((target_price-current_price)/stdev,2)
    if target_price <= (-2*stdev + current_price):
        return ("Strong Sell. Target price (" + 
                str(round(target_price,2)) + 
                ") is " + 
                str(distance) + 
                " stdev from the current price (" + 
                str(round(current_price,2)) + ").")
    elif target_price <= (-1*stdev + current_price):
        return ("Sell. Target price (" + 
                str(round(target_price,2)) + 
                ") is " + 
                str(distance) + 
                " stdev from the current price (" + 
                str(round(current_price,2)) + ").")
    elif target_price <= (stdev + current_price):
        return ("Hold. Target price (" + 
                str(round(target_price,2)) + 
                ") is " + 
                str(distance) + 
                " stdev from the current price (" + 
                str(round(current_price,2)) + ").")
    elif target_price <= (2*stdev + current_price):
        return ("Buy. Target price (" + 
                str(round(target_price,2)) + 
                ") is " + 
                str(distance) + 
                " stdev from the current price (" + 
                str(round(current_price,2)) + 
                ").")
    elif (2*stdev + current_price) < target_price :
        return ("Strong Buy. Target price (" + 
                str(round(target_price,2)) + 
                ") is " + 
                str(distance) + 
                " stdev from the current price (" + 
                str(round(current_price,2)) + 
                ").")
    else:
        return ("ERROR!")

#%%
def convert(num):
    """Returns currency formatted string for printing."""
    return '${:0,.0f}'.format(num).replace('$-','-$')