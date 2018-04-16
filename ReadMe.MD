##### DISCLAIMER: This calculator is designed to be a informational and educational tool only, and when used alone, do not constitute investment advice. The results presented by this calculator are hypothetical and may not reflect the actual value of stocks. We are not responsible for the consequences of any decisions or actions taken in reliance upon or as a result of the information provided by these tools. We are not responsible for any human or mechanical errors or omissions. Use this at your own risk.
******

#### You will need your own Quandl API key to operate this application. [Create a free quandl account here](https://www.quandl.com/) 


# Getting Started
1. Download and install Python from this website:
	https://www.python.org/downloads/

2. Install / ensure the following packages are installed:
	1. `pandas`
	
	2. `pandas_datareader`
	
	3. `numpy`
	
	4. `dateutil`
	
	5. `datetime`
	
	6. `sys`
	
	7. `PyQt5`
	
	8. `quandl`
	
	**If you are using Anaconda run the command below for each package in the Anaconda Prompt:**
		
		conda install pandas
		
	
	
	
	**If you are not using any package manager:**
		
		
	i. Install pip by following instructions from this website:
			https://pip.pypa.io/en/stable/installing/
	
	
	ii. Run the command below in your terminal to install each package:
	
		pip install pandas
		
	Repeat step ii for all packages
		
3. Extract the zip file into a single folder. From your terminal, change the directory to that folder and execute the command below to run the application

		python ./Main.py
		
	This should open a new window ("MainWindow")
	
4. Input the `Stockticker` (required), `Forecasted Growth Rate` (optional), `Perpetual Growth Rate` (optional), and `Quandl API key` (required).

	a. An invalid stockticker will cause the program to crash. Please input valid stocktickers
	
	- Invalid stocktickers: `AAPL`, `GOOG`, `MMM`, `BNP.PA`
	
	- Valid stocktickers: `FB`, `AMZN`, `TSLA`, `XOM`

	b. `Forecasted Growth Rate` and `Perpetual Growth Rate` are `0.25` and `0.03` respectively by default, even when empty
	
	c. An invalid input on the growth rates (i.e. text format) will cause the program to crash. Please input valid growth rates
	
	d. An invalid or empty `Quandl API Key` will cause an error. Please create an account with Quandl and input your own API key. 
	
5. Click 'Calculate'. The code will take some time to run

6. The program will output the financial results from the valuation algorithm and other financial data from its data sources. 

7. You can run the program again **ONLY FOR VALID INPUTS** by having different inputs and clicking 'Calculate' again. If you are unsure if the inputs are valid, **CLOSE THE APPLICATION** and run it again 
