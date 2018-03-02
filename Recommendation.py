# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 15:19:05 2018

@author: Sherman

Recommends Buy/Sell/Hold based on DCF valuation and stock price

Input -- DCF valuation at present value
Output -- one of the following: "Strong Sell", "Sell", "Hold", "Buy", "Strong Buy"
"""

#Import Packages and Modules ------------------------------------------------------------------------------------
import pandas as pd
import pandas_datareader.data as pdr
import requests
from datetime import datetime

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
valuation = 1_000_000_000_000

#Data Collection ------------------------------------------------------------------------------------

prices = pdr.DataReader('AMZN','yahoo',datetime)
