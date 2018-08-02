# main.py

# Import the modules 
import sys
sys.path.append("./modules") # Add the sub folder
from common import init # must be before everything else
from ReadWrite import readSheet, printValues, editRecord

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

editRecord(record, range = '')

	changes a record

	record is required
	must be a list object

	range is optional
	describes where it writes the record
	if none give default is used

'''



def main():

	printValues() # Baisic action

	# Do something





if __name__ == '__main__':
	init() # Must always be run first
	main()