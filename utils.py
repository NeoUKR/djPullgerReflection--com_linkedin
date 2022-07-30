import csv
from djPullgerReflection.com_linkedin import metods
from pyPullgerFootPrint.com.linkedin import general
import re


def loadCSV():
    file = open('ConvertedUTF.csv', newline='', encoding='utf-8')
    csvreader = csv.reader(file, delimiter=";", dialect=csv.excel)

    rowCount = 0
    for row in csvreader:
        rowCount += 1

        try:
            if len(row) == 18:
                # splitedCSV = row[0].split(';')
                splitedCSV = row

                name = splitedCSV[0].strip()

                url = splitedCSV[2]
                url = general.getCleanedURL(url)

                if url != None:
                    id = general.getIdFromURL(url)
                    nick = general.getNickFromURL(url)

                    revenue = None
                    revenueString = splitedCSV[3]
                    regRev = re.findall(r'\d+(?:\.\d+)?', revenueString)

                    try:
                        if len(regRev) == 1:
                            revenueInt = int(regRev[0])
                        elif len(regRev) > 1:
                            revenueInt = int(regRev[1])
                        else:
                            revenueInt = 0
                    except:
                        revenueInt = 0

                    revenueInt = revenueInt*1000000

                    companyDict = {
                        "id": id,
                        "nick": nick,
                        "name": name,
                        "url": url,
                        "dnb_revenue": revenueInt,
                        "searcher": "outsource",
                        "outsource_industry": True
                    }

                    if id != None or nick != None:
                        try:
                            newCompany = metods.addCompany(**companyDict)
                        except Exception as e:
                            print(f'Error in line {rowCount} : {str(e)}')
                    else:
                        print('Error data')
                else:
                    print(f'Incorrect url in line {rowCount} ')
            else:
                print(f'Incorrect line {rowCount}')
        except Exception as e:
            print(f'Error in line {rowCount} : {str(e)}')