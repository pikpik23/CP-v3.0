# main.py

# Import the modules 
import sys
sys.path.append("./modules") # Add the sub folder
from common import init
from ReadWrite import readSheet, printValues, editRecord


if __name__ == '__main__':
	init()
	printValues()

	# Do something