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

    def PB_C(self,):
        #clear recommendation bar
        self.output_rec.setText('')
    #getting the inputs
        stockticker = self.input_stockticker.text()
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
                ignore = quandl.Dataset('WIKI/AAPL').data()
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
        #except:
#            self.output_rec.setText('Error: Invalid Quandl API key. ' +
#                                    'Please check your API key '+
#                                    'and try again')
#            exit
            
        company = Company(stockticker,quandl.ApiConfig.api_key)
        data = company.data
    #generate the outputs
        #ebit - imported as a variable
        self.output_ebit.setText(d.convert(data['lastebit'])) 
        #tax rate
        atr = d.avg_tax_rate(data['taxexp'],data['ebt'])
        self.output_tax_rate.setText(str(round(atr,4)))
        #depreciation and amortization - imported as a variable
        self.output_depr.setText(d.convert(data['dep']))
        self.output_amor.setText(d.convert(data['amor']))
        #capital expenditure - imported as a variable
        self.output_capex.setText(d.convert(data['capex']))
        #change in networking capital
        cwc = d.cwc(data['ybca'],data['yeca'],data['ybcl'],data['yecl'])
        self.output_cwc.setText(d.convert(cwc))
        #fcf valuation
        fcf = d.fcf(data['lastebit'],
                    atr,
                    data['dep'],
                    data['amor'],
                    cwc,
                    data['capex'])
        self.output_fcf.setText(d.convert(fcf))
        #5 years free cash flow 
        #outputs all five years as a tuple 
        #(convert to list, then return individual years)
        fiveyearfcf = {}
        if forecasted_growth_rate is None:
            fiveyearfcf = d.five_year_fcf(fcf)
        else:
            fiveyearfcf = d.five_year_fcf(fcf,forecasted_growth_rate)
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
        #cost of equity
        re = d.re(data['rm'],data['rf'],data['beta'])
        self.output_coe.setText(str(round(re,4)))
        #total long term debt - imported as a variable
        self.output_ltd.setText(d.convert(data['lastD']))
        #cost of debt
        rd = d.rd(data['intexp'],data['LTD'])
        self.output_cod.setText(str(round(rd,4)))
        #weighted average cost of capital
        wacc = d.wacc(data['marketcap'],data['lastD'],atr,re,rd)
        self.output_wacc.setText(str(round(wacc,4)))
        #terminal value - not part of ui, but included in calculation
        tv = 0
        if perpetual_growth_rate is None:
            tv = d.tv(fiveyearfcf,wacc)
        else:
            tv = d.tv(fiveyearfcf,wacc, perpetual_growth_rate)
        #discounted cash flow for the current year
        dcf = d.dcf(fiveyearfcf,wacc,tv)
        self.output_dcf.setText(d.convert(dcf))
        #target price - not part of ui, but included in calculation
        target_price = d.target_price(dcf,data['lastD'],data['numshares'])
        #recommendation
        rec = d.recommendation(
                data['current_price'],data['stdev'],target_price)
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