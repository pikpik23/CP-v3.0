from mailmerge import MailMerge
import datetime
from sheetsBackend import Sheet #Custom Google Api class

# SHEET ID CODES
dataFileID = "1B0_wRMWrI40_i_jH_RlPbk-Lz8OeknMnqX2RQbFSkrg"
tpFileID = "1p3sBzEcor9QXPsX5LyDFluFHh4EjkZNGijVbAJZgkGg"

dataFile = Sheet(dataFileID, "data")


curOrderNum = 3

dressOrderCodes = [{'who':'code'},{"test":"1"}]

template = "RO_TEMPLATE.docx"
document = MailMerge(template)

def readDressOrders():
	dic = dict()
	for code, lCode, codeDesc in dataFile.readSheet(CellRange="dressCodes"):
		dic.update({code:{'codeLong':lCode,'codeDesc': codeDesc}})
	return dic


dressOrders = readDressOrders()

def testWrite():
	#next firday date
	d = datetime.date.today()
	while d.weekday() != 4:
		d += datetime.timedelta(1)

	field = dict()

	#Handle the baisic merges
	for x in document.get_merge_fields():
		skip = False

		if "orderNum" in x:
			i  = curOrderNum + int(x.split(".")[1])
			val = '{:03}'.format(i)
			field.update({x:val})

		elif "date" in x:
			sub = x.split(".")[1]
			if sub == "date":
				val = d.strftime("%d")
			elif sub == "super":
				num = d.strftime("%d")
				if num == 1:
					val = 'st'
				elif num == 2:
					val = 'nd'
				elif num == 3:
					val = 'rd'
				else:
					val = 'th'
			elif sub == "month":
				val = d.strftime("%B")
			elif sub == "year":
				val = d.strftime("%Y")
			else:
				skip = True
		else:
			skip = True

		if not skip:
				field.update({x:val})
		

	#Handle the Dress table
	dress_lst = list()

	# generate random dress inputs
	for dic in dressOrderCodes:
		for who, code in dic.items():
			dress_entry = dict()
			dress_entry.update({"dress.rank":who})
			dress_entry.update({"dress.name":dressOrders[code]['codeLong']})
			dress_entry.update({"dress.desc":dressOrders[code]['codeDesc']})
		
		#add to dress list
		dress_lst.append(dress_entry)

	document.merge(**field)
	document.merge_rows("dress.rank", dress_lst)

	document.write('test-output.docx')



if __name__ == "__main__":
	#print(dressOrders)
	testWrite()
	#print(document.get_merge_fields())