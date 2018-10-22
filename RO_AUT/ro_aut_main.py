from mailmerge import MailMerge
import datetime
from sheetsBackend import Sheet #Custom Google Api class

# SHEET ID CODES
dataFileID = "1B0_wRMWrI40_i_jH_RlPbk-Lz8OeknMnqX2RQbFSkrg"
tpFileID = "1p3sBzEcor9QXPsX5LyDFluFHh4EjkZNGijVbAJZgkGg"

tpSheetName="'T4 W2'"

dataFile = Sheet(dataFileID, "data")
tpData = Sheet(tpFileID, tpSheetName+"!A:E").readSheet()

curOrderNum = 3


SENIOR_PLATOONS = {"ADMIN": "ADMIN",
                   "QUARTERMASTERS": "QM",
                   "OPERATIONS": "OPS",
                   "MEDICS": "MED",
                   "SIGNALLERS": "SIG",
                   "ENGINEERS": "ENG",
                   "PIONEERS": "PNR"}

SENIOR_COY_FINDER = {"ADMIN":"HQ",
                   "QM":"HQ",
                   "OPS": "HQ",
                   "MED":"SPT",
                   "SIG":"SPT",
                   "ENG":"SPT",
                   "PNR":"SPT"}

template = "RO_TEMPLATE.docx"
document = MailMerge(template)


def testWrite():
    # next firday date
    d = datetime.date.today()
    while d.weekday() != 4:
        d += datetime.timedelta(1)

    field = dict()

    # Handle the baisic merges
    for x in document.get_merge_fields():
        val = None
        skip = False

        if "orderNum" in x:
            i = curOrderNum + int(x.split(".")[1])
            val = '{:03}'.format(i)
            field.update({x: val})

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
            field.update({x: val})

    # Handle the Dress table
    dress_lst = list()
    dress_entry = dict()

    # generate random dress inputs
    for dic in dressOrderCodes:
        for who, code in dic.items():
            dress_entry = dict()
            dress_entry.update({"dress.rank": who})
            dress_entry.update({"dress.name": DRESS_ORDERS[code]['codeLong']})
            dress_entry.update({"dress.desc": DRESS_ORDERS[code]['codeDesc']})

        # add to dress list
        dress_lst.append(dress_entry)

    document.merge(**field)
    document.merge(**TP_MERGE)
    document.merge_rows("dress.rank", dress_lst)

    document.write('test-output.docx')


def readDressOrders():
	dic = dict()
	for code, lCode, codeDesc in dataFile.readSheet(CellRange="dressCodes"):
		dic.update({code:{'codeLong':lCode,'codeDesc': codeDesc}})
	return dic


def getTPdata():
    tpDic = dict()
    pls = [4,8,12,16,20]
    coys = ["B","C","D","E","F"]
    index = 0
    for i in tpData:
        for pl in pls:
            if i:
                if i[0] == str(pl)+" PL": # REC COY
                    coy = coys[(int(pl/4)-1)]

                    keyTRG = str(f"{coy}.1.TRG")
                    keyLOC = str(f"{coy}.1.LOC")
                    tpDic.update({keyTRG: convertTRG_REC(i[1])})
                    tpDic.update({keyLOC: i[2]})

                    keyTRG = str(f"{coy}.2.TRG")
                    keyLOC = str(f"{coy}.2.LOC")
                    tpDic.update({keyTRG: convertTRG_REC(i[3])})
                    tpDic.update({keyLOC: i[4]})

                elif "A COY" in i[0]: # A COY
                    tier = int(i[0].split(" TIER ")[1])
                    coy = 'A'
                    keyTRG = str(f"{coy}.1.{tier}.TRG")
                    keyLOC = str(f"{coy}.1.{tier}.LOC")
                    tpDic.update({keyTRG: i[1]})
                    tpDic.update({keyLOC: i[2]})

                    keyTRG = str(f"{coy}.2.{tier}.TRG")
                    keyLOC = str(f"{coy}.2.{tier}.LOC")
                    tpDic.update({keyTRG: i[3]})
                    tpDic.update({keyLOC: i[4]})

                elif i[0].split(" ")[0] in SENIOR_PLATOONS: # THE REST

                    coy = SENIOR_COY_FINDER[SENIOR_PLATOONS[i[0].split(" ")[0]]]
                    pl = SENIOR_PLATOONS[i[0].split(" ")[0]]

                    try:
                        tier = int(i[0].split(" TIER ")[1])
                    except IndexError:
                        tier = 1

                    keyTRG = str(f"{coy}.{pl}.1.{tier}.TRG")
                    keyLOC = str(f"{coy}.{pl}.1.{tier}.LOC")
                    tpDic.update({keyTRG: i[1]})
                    tpDic.update({keyLOC: i[2]})

                    keyTRG = str(f"{coy}.{pl}.2.{tier}.TRG")
                    keyLOC = str(f"{coy}.{pl}.2.{tier}.LOC")
                    tpDic.update({keyTRG: i[3]})
                    tpDic.update({keyLOC: i[4]})

    return tpDic

def getDefs(range):
    codes = list()
    first = True
    for key, val in dataFile.readSheet(range):
        if not first:
            codes.append({key: val})
        else:
            first = False
    return codes

def getDic(range):
    codes = dict()
    first = True
    for key, val in dataFile.readSheet(range):
        if not first:
            codes.update({key: val})
        else:
            first = False
    return codes


def convertTRG_REC(codes):

    desc = list()
    for code in codes.split(" / "):
        if code in TRG_CODES:
            desc.append(TRG_CODES[code])

    if desc:
        codes = str(f"{codes} - {' / '.join(desc)}")


    return codes

TRG_CODES = getDic("lessonCodes!A:B")
TP_MERGE = getTPdata()
DRESS_ORDERS = readDressOrders()
dressOrderCodes = getDefs("currentDress!A:B")

if __name__ == "__main__":

    #print(TRG_CODES)
    #print(TP_MERGE)
    #print(tp_merge)
	#print(dressOrders)
    testWrite()
    #print(document.get_merge_fields())