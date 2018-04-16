"""
This is the Main file. Run this to start the application

Created 23 March 2018

@authors:
    Ng Hao Wei (haowei.ng.2014)
    Dylan Chan (dylan.chan.2016)
    Nurul Suhailah Binte Sapnan (suhailahs.2015)
"""

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
from Company import Company
import dcffunctions as d
import quandl

qtCreatorFile = "qf205guiProject.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.input_stockticker.setText('AMZN')
        self.input_forecastedGrowthRate.setText('0.25')
        self.input_perpetualGrowthRate.setText('0.03')
        self.input_quandl_API_key.setText('')

        self.pushButton_calculate.clicked.connect(self.PB_C)

    def clearOutputs(self):
        """ Clears all outputs on GUI. """
        self.output_rec.setText('')
        self.output_ebit.setText('') 
        self.output_tax_rate.setText('')
        self.output_depr.setText('')
        self.output_amor.setText('')
        self.output_capex.setText('')
        self.output_cwc.setText('')
        self.output_fcf.setText('')
        self.output_y0.setText('')
        self.output_y1.setText('')
        self.output_y2.setText('')
        self.output_y3.setText('')
        self.output_y4.setText('')
        self.output_y5.setText('')
        self.output_marketcap.setText('')
        self.output_beta.setText('')
        self.output_emr.setText('') 
        self.output_coe.setText('')
        self.output_ltd.setText('')
        self.output_cod.setText('')
        self.output_wacc.setText('')
        self.output_dcf.setText('')
        
    
    def PB_C(self,):
    # clear all outputs
        self.clearOutputs()
        
    #getting the inputs and exception handling
        if self.input_stockticker.text() is not '':
            stockticker = self.input_stockticker.text()
        else:
            self.output_rec.setText('Error: Please input a stockticker.')
            raise
            exit

        if self.input_forecastedGrowthRate.text() is not '':
            forecasted_growth_rate = float(
                    self.input_forecastedGrowthRate.text())
        else:
            forecasted_growth_rate = None

        if self.input_perpetualGrowthRate.text() is not '':
            perpetual_growth_rate = float(
                    self.input_perpetualGrowthRate.text())
        else:
            perpetual_growth_rate = None
            
        if self.input_quandl_API_key.text() is not '':
            quandl.ApiConfig.api_key = self.input_quandl_API_key.text()
        else:
            self.output_rec.setText('Error: Please input an Quandl API Key.'+ 
                                    ' Go to https://www.quandl.com/')
            raise
            exit
        
        #test if quandl apikey is valid
        count = 0
        while True:
            try:
                quandl.Dataset('WIKI/AAPL').data()
                break
            except:
                count += 1
                if count >8:
                    self.output_rec.setText('Error: Invalid Quandl API key. ' +
                                        'Please check your API key '+
                                        'and try again')
                    raise
                    exit
                
        #test if stockticker is valid
        count = 0
        while True:
            try:
                ignore = quandl.Dataset('WIKI/' + stockticker).data()
                break
            except:
                count += 1
                if count >8:
                    self.output_rec.setText('Error: Invalid stockticker.')
                    raise
                    exit
        
    #initialise Company object and store 'data' attribute [dict]
        company = Company(stockticker,quandl.ApiConfig.api_key)
        data = company.data
        
        
    # Calculations using Company data and dcffunctions
        #tax rate
        atr = d.avg_tax_rate(data['taxexp'],data['ebt'])
        #change in networking capital
        cwc = d.cwc(data['ybca'],data['yeca'],data['ybcl'],data['yecl'])
        #fcf valuation
        fcf = d.fcf(data['lastebit'],
                    atr,
                    data['dep'],
                    data['amor'],
                    cwc,
                    data['capex'])
        #5 years free cash flow 
        #outputs all five years as a tuple 
        #(convert to list, then return individual years)
        fiveyearfcf = {}
        if forecasted_growth_rate is None:
            fiveyearfcf = d.five_year_fcf(fcf)
        else:
            fiveyearfcf = d.five_year_fcf(fcf,forecasted_growth_rate)
        #cost of equity
        re = d.re(data['rm'],data['rf'],data['beta'])
        #cost of debt
        rd = d.rd(data['intexp'],data['LTD'])
        #weighted average cost of capital
        wacc = d.wacc(data['marketcap'],data['lastD'],atr,re,rd)
        #terminal value - not part of ui, but included in calculation
        tv = 0
        if perpetual_growth_rate is None:
            tv = d.tv(fiveyearfcf,wacc)
        else:
            tv = d.tv(fiveyearfcf,wacc, perpetual_growth_rate)
        #discounted cash flow for the current year
        dcf = d.dcf(fiveyearfcf,wacc,tv)
        #target price - not part of ui, but included in calculation
        target_price = d.target_price(dcf,data['lastD'],data['numshares'])
        #recommendation
        rec = d.recommendation(
                data['current_price'],data['stdev'],target_price)
        
        
        

        
    #generate the outputs
        #ebit - imported as a variable
        self.output_ebit.setText(d.convert(data['lastebit'])) 
        self.output_tax_rate.setText(str(round(atr,4)))
        #depreciation and amortization - imported as a variable
        self.output_depr.setText(d.convert(data['dep']))
        self.output_amor.setText(d.convert(data['amor']))
        #capital expenditure - imported as a variable
        self.output_capex.setText(d.convert(data['capex']))
        self.output_cwc.setText(d.convert(cwc))
        self.output_fcf.setText(d.convert(fcf))
        self.output_y0.setText(d.convert(fiveyearfcf[0]))
        self.output_y1.setText(d.convert(fiveyearfcf[1]))
        self.output_y2.setText(d.convert(fiveyearfcf[2]))
        self.output_y3.setText(d.convert(fiveyearfcf[3]))
        self.output_y4.setText(d.convert(fiveyearfcf[4]))
        self.output_y5.setText(d.convert(fiveyearfcf[5]))
        #market capitalization - imported as a variable
        self.output_marketcap.setText(d.convert(data['marketcap']))
        #beta - imported as a variable
        self.output_beta.setText(str(data['beta']))
        #expected market returns - imported as a variable
        self.output_emr.setText(str(round(data['rm'],4))) 
        self.output_coe.setText(str(round(re,4)))
        #total long term debt - imported as a variable
        self.output_ltd.setText(d.convert(data['lastD']))
        self.output_cod.setText(str(round(rd,4)))
        self.output_wacc.setText(str(round(wacc,4)))
        self.output_dcf.setText(d.convert(dcf))
        self.output_rec.setText(rec) #insertPlainText


    #runs the GUI when 'run.py' is initiated using Python 3.6
    #usable and importable, 
    #command line runs if the module is executed as the 'main' file
if __name__ == '__main__':

    app = QApplication(sys.argv)
    main = Main()
    main.show()
    #app.exec_() causes the program to enter the mainloop
    #Syst.exit() exits the mainloop.
    sys.exit(app.exec_())