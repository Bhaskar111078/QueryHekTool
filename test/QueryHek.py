# A QueryHek takes a path to input configuration file (including file name) and path to output folder
# and generates a XML or JSON file by querying HEK API. A query is constructed from the given search conditions in input configuration file
# @author Bhaskar Ray
# @version 09/18/2018

import urllib.request
import urllib.parse
import re

url = 'https://www.lmsal.com/hek/her?cosec=1&&cmd=search&type=column'

'''
fileName
startTime,endTime
startHour,startMinute,startSecond,endHour,endMinute,endSecond
startYear,startMonth,startDay
endYear,endMonth,endDay
filterCount
xmlFlag
jsonFlag
recordCount
'''

startYear=''
startMonth=''
startDay=''
startHour=''
startMinute=''
startSecond=''
endYear=''
endMonth=''
endDay=''
endHour=''
endMinute=''
endSecond=''
eventModuleString=''
coordinateValue=''
x1Value=''
x2Value=''
y1Value=''
y2Value=''
eventModule = []
eventCoordSystem = []
filterCondition = []
filterConditionValue = []
filterValues = []
filterOperators = []
filterData=[]

EVENT_REGION = 'all'
RESULT_LIMIT = '200'
ENCODING_SCHEME = 'utf-8'
REQUIRED_PARAMETERS = 6

try:

    inputFileName = input("Enter input file path with file name: ")
    opDirectory = input("Enter output directory path: ")
    # lines = [line.rstrip('\n') for line in open(inputFileName, 'r')]

    with open(inputFileName, 'r') as f:
        contents = f.readlines()
        f.close()
    contents = [content.strip('\n') for content in contents]
    # print("Content: ", contents)
    # tokens = [token.split(':') for token in contents]
    # print("Token:", tokens)
    # print("Token:", tokens[0])

    # for i in range(0, len(contents)):
    #     tokens = []
    #     tokens=contents[i].split(':')
    #     print("Token zero: ", tokens[0])
    #     print("Token one: ", tokens[1])



    for token in contents:

        tokens = token.split(':')
        print("Token zero: ", tokens[0])
        print("Token one: ", tokens[1])

        # print("Token zero: ", tokens[0])
        # print("Token one: ", tokens[1])
        #
        #
        # # print("Total length: ",len(contents))
        # print(tokens)
        if 'Start Date' in tokens[0]:
            for tokenValue in tokens:
                if '-' in tokenValue:
                    ymd = tokenValue.split('-')
                    print("YMD: ", ymd)
                    print("YMD zero", ymd[0])
                    print("YMD one", ymd[1])
                    print("YMD two", ymd[2])
                    startYear = ymd[0].strip()
                    startMonth = ymd[1].strip()
                    startDay = ymd[2].strip()

        elif 'End Date' in tokens[0]:

            for tokenValue in tokens:
                if '-' in tokenValue:
                    ymd = tokenValue.split('-')
                    print("YMD: ", ymd)
                    endYear = ymd[0].strip()
                    endMonth = ymd[1].strip()
                    endDay = ymd[2].strip()

        elif 'Start Time' in tokens[0]:
            for tokenValue in tokens:
                if '-' in tokenValue:
                    hms = tokenValue.split('-')
                    print("HMS: ", hms)
                    startHour = hms[0].strip()
                    startMinute = hms[1].strip()
                    startSecond = hms[2].strip()

        elif 'End Time' in tokens[0]:
            for tokenValue in tokens:
                if '-' in tokenValue:
                    hms = tokenValue.split('-')
                    print("HMS: ", hms)
                    endHour = hms[0].strip()
                    endMinute = hms[1].strip()
                    endSecond = hms[2].strip()

        elif 'Event Type' in tokens[0]:
            eventModule = [tokens[1].split(',')]

            print("eventModule: ",eventModule)
            eventModuleString = "'" + "','".join(map(str, eventModule[0])) + "'"
            # eventModuleString = "','".join(map(str, eventModule[0]))
            print("eventModuleString: ",eventModuleString)

        elif 'Spatial Region' in tokens[0]:
            for tokenValue in tokens:
                if ',' in tokenValue:
                    event = tokenValue.split(',')
                    coordinateValue=event[0].strip()
                    x1Value=event[1].strip()
                    x2Value=event[2].strip()
                    y1Value=event[3].strip()
                    y2Value=event[4].strip()


        else:

            filterCondition.append(tokens[0].strip())
            opVal = tokens[1].split(',')
            filterOperators.append( opVal[0].strip())
            filterConditionValue.append(opVal[1].strip())
            print(tokens)
            print("FilterCondition: ",filterCondition)
            print("FilterOperators: ", filterOperators)
            print("filterConditionValue: ", filterConditionValue)
        # print("Token: ", tokens)
        # print("Token Index zero: ", tokens[0])
        # print("Token Index one: ", tokens[1])

    # ymd =[x.split('-') for x in token]
    # print("TokenNew", ymd)
    # startYear = ymd[0]
    # startMonth = ymd[1]
    # startDay = ymd[2]
    # print("StartYear", ymd[0])
    # print("StartMonth", ymd[1])
    # print("StartDay", ymd[2])



except Exception as e:
    print("Input Error: ", str(e))


try:

    # for i in range(0, len(filterCondition)):

    i=0
    for filterCount in filterCondition:
        filterData.append("{0},{1},{2}".format("'"+'sparam'+ str(i)+"'"+':'+"'"+filterCondition[i]+"'","'"+'op'+ str(i)+"'"+':'+"'"+filterOperators[i]+"'","'"+'value'+ str(i)+"'"+':'+"'"+filterConditionValue[i]+"'"))
        # print(i)
        i=i+1
        # print(i)
    print("Filter Data: ", filterData[0])
    print("Filter Data: ", filterData[1])

except Exception as e:
    print("Exception in loop: ", str(e))

#
# try:
#     i=0
#     values1="{"
#     values1 = +"{0}".format("}")
#     # for moduleEach in eventModule:
#     #     values1=+"{0}".format(eventModule[i])
#     #     # if i<len(eventModule)-1:
#     #     values1=+"{0}".format(",")
#     #     i=i+1
#     print(values1)
#
#
# except Exception as e:
#     print("Exception : ", str(e))









try:

    # values = {'event_type': 'ar,sg,fl,fi', 'event_region': EVENT_REGION, 'event_coordsys': "'" + coordinateValue + "'",
    #           'x1': "'" + x1Value + "'", 'x2': "'" + x2Value + "'",
    #           'y1': "'" + y1Value + "'", 'y2': "'" + y2Value + "'", 'result_limit': "'" + RESULT_LIMIT + "'",
    #           'event_starttime': "'" + startYear + '-' + startMonth + '-' + startDay + 'T' + startHour + ':' + startMinute + ':' + startSecond + "'",
    #           'event_endtime': "'" + endYear + '-' + endMonth + '-' + endDay + 'T' + endHour + ':' + endMinute + ':' + endSecond + "'"}

    values = {'event_type': 'ar,sg,fl,fi', 'event_region': EVENT_REGION, 'event_coordsys': coordinateValue,
              'x1': x1Value, 'x2': x2Value,
              'y1': y1Value, 'y2': y2Value, 'result_limit': RESULT_LIMIT,
              'event_starttime': startYear + '-' + startMonth + '-' + startDay + 'T' + startHour + ':' + startMinute + ':' + startSecond,
              'event_endtime': endYear + '-' + endMonth + '-' + endDay + 'T' + endHour + ':' + endMinute + ':' + endSecond + "," + ",".join(
                  map(str, filterData))}

    print(values)
    data = urllib.parse.urlencode(values)
    data = data.encode(ENCODING_SCHEME)
    # print(data)
    req = urllib.request.Request(url,data)
    req = urllib.request.Request(url)
    # print(req)
    resp = urllib.request.urlopen(req)
    resData = resp.read()

    # fileName = "Temp" + eventModule[0]+ "_event_startdate=" + startYear.strip() + "-" + startMonth.strip() + "-" + startDay.strip() + "T" + startTime.trim() + "event_enddate=" + endYear.trim() + "-" + endMonth.trim() + "-" + endDay.trim() + "T" + endTime.trim() + ".json";
    saveFile= open('F:\pytest\Value.xml', 'w')
    saveFile.write(str(resData))
    saveFile.close()

except Exception as e:

    print('Error:', str(e))







# filterValueList ={'sparam0':'FRM_Contact','op0':'=','value0': 'veronique.delouille@sidc.be'}


# Do something with 'line'


# url= 'https://www.lmsal.com/hek/her?cosec=2&&cmd=search&type=column&event_type=ar,fl,sg&event_region=all&event_coordsys=helioprojective&x1=-5000&x2=5000&y1=-5000&y2=5000&result_limit=200&event_starttime=2018-03-17T00:00:00&event_endtime=2018-04-17T23:59:59'


# query='&event_type=ar,ce,ch,cj,cw,fi,fe,fa,fl,os,sg,sp&event_region=all&event_coordsys=helioprojective&x1=-5000&x2=5000&y1=-5000&y2=5000&result_limit=120&event_starttime=2018-03-17T00:00:00&event_endtime=2018-04-17T23:59:59&sparam0=ch.area_atdiskcenter&op0=>&value0=608735000'
#
# quoted_query= urllib.parse.urlencode(query)
# url=url+quoted_query





# paragraphs = re.findall(r'<p>(.*?)</p>', str(resData))
#
# for eachP in paragraphs:
#     print(eachP)


