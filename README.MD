Instructions on operating the DCF calculator application

The zip file contains 4 files (excluding this ReadMe.txt): Main.py, Company.py, dcffunctions.py, qf205guiProject.ui

#Getting Started
1. Download and install Python from this website:
	https://www.python.org/downloads/

2. Install / ensure the following packages are installed:
	a. pandas
	b. pandas_datareader
	c. numpy
	d. dateutil
	e. datetime
	f. sys
	g. PyQt5
	
	If you are using Anaconda run the command below for each package in the Anaconda Prompt:
		
		conda install pandas
		
	
	If you are not using any package manager:
		i. Install pip by following instructions from this website:
			https://pip.pypa.io/en/stable/installing/
		ii. Run the command below in your terminal to install each package:
	
			pip install pandas
			
		iii. Repeat step ii for all packages
		
3. Extract the zip file into a single folder. From your terminal, change the directory to that folder and execute the command below to run the application

		python ./Main.py
		
	This should open a new window ("MainWindow")
	
4. Input the Stockticker, Forecasted Growth Rate (optional) and Perpetual Growth Rate (optional). 'AMZN' is the default value as the stockticker; change this for a different stockticker.
	a. An invalid stockticker will cause the program to crash. Please input valid stocktickers
	b. Forecasted Growth Rate and Perpetual Growth Rate are 0.25 and 0.03 respectively by default
	c. A invalid input on the growth rates (i.e. text format) will cause the program to crash. Please input valid growth rates
	
5. Click 'Calculate'. The code will take some time to run. Occasionally an error message for pdr.get_data_yahoo() may appear on the terminal prompt. Ignore this message and allow the program to run.

6. The program will output the financial results from the valuation algorithm and intermediate financial data from its data sources. 

7. You can run the program again by having other values in the input fields and clicking 'Calculate' again.