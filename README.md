# Command Post v3.0

* This repository includes a series of random Cadet related programs, mainly the new Command Post Software.

## Viewing CP 3.0
**Prerequisites**
* [Git](https://git-scm.com/)
* [Pip](https://pip.pypa.io/en/stable/installing/)

**Installation**
* `git clone https://github.com/pikpik23/CP-v3.0/`
* `cd CP-v3.0/CP\ Software`
* `pip3 install -r requirements.txt`

**Running**
* `./app.py`




## Depreciated
## Instructions

**Making changes:**
* Changes can be made to master if it is a minor fix, or addition of completed module

* if you want to experiment and go on tangents make a branch. 
  * (You can then merge it in if it is successful)

**Layout of project**
* main.py 
  * where our modules are run from
    * should have complete abstraction
    * contains a small description of the linked functions
    * this is the file that you use to start the program
    
* ReadWrite.py
  * Contains
    * readSheet
    * printValues
    * editTable
* Common.py
  * Contains
    * SCOPES
      * The permissions of the API
    * SPREADSHEET_ID
      * The ID of the spreadsheet (found in url)
    * value_input_option
      * Ignore (Just tells api how to handle input)
    * totalRange
    	* The default Range
    * service
      * The Var where temp auth is stored (Hopefully this makes it faster if calling multiple functions)

**Functions**
* readSheet(range = '')
	
	* returns a list of items in provided range
	
	* range is optional
	* if no range is provided it reads the default range

* printValues(list = '', header=["Names", "Number"])

	* prints the list provided
	
	* list optional
	  *if no list is provided it prints the default range (see readSheet)

	* header optional
	  * effects the column headings that get printed

* editTable(record, range = '')

	* Rewrites the table
	  * IMPORTANT: This overwrites cells if range is wrong

	* record is required
	  * must be a 2d list object
	  * eg: *data = [["fred",123],["john",453]]*

	* range is optional
	  * describes where it writes the record
	  * if none give default is used

**Folders:**
* Complete is for the currently working Modules and Main.
* WIP is for modules that work but aren't useful
