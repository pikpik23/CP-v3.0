# main.py

# Import the modules 
import sys
sys.path.append("./modules") # Add the sub folder
from common import init # must be before everything else
from ReadWrite import readSheet, printValues, editTable

'''
Description of functions:

readSheet(range = '')
	
	returns a list of items in provided range
	
	range is optional
	if no range is provided it reads the default range

printValues(list = '', header=["Names", "Number"])

	prints the list provided
	
	list optional
	if no list is provided it prints the default range (see readSheet)

	header optional
	effects the column headings that get printed

editTable(record, range = '')

	Rewrites the table
	IMPORTANT: This overwrites cells if range is wrong

	record is required
	must be a 2d list object
	eg: data = [["fred",123],["john",453]]

	range is optional
	describes where it writes the record
	if none give default is used

'''



def main():

	data = [["fred",123],
			["john",453],
			["Bob", 567]]

	editTable(data)
	printValues()


	# Do something





if __name__ == '__main__':
	init() # Must always be run first
	main()