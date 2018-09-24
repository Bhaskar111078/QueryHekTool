# A QueryHek takes a path to input configuration file (including file name) and path to output folder
# and generates a XML or JSON file by querying HEK API. A query is constructed from the given search conditions in input configuration file
# @author Bhaskar Ray
# @version 09/25/2018

import urllib.request
import urllib.parse



def main():


    startYear = ''
    startMonth = ''
    startDay = ''
    startHour = ''
    startMinute = ''
    startSecond = ''
    endYear = ''
    endMonth = ''
    endDay = ''
    endHour = ''
    endMinute = ''
    endSecond = ''
    coordinateValue = ''
    x1Value = ''
    x2Value = ''
    y1Value = ''
    y2Value = ''
    eventModuleString = ''
    filterCondition = []
    filterConditionValue = []
    filterOperators = []
    valuesLoop = []
    fileName=''
    opDirectory=''
    json = False
    xml = False
    url = ''
    EVENT_REGION = 'all'
    RESULT_LIMIT = '200'
    ENCODING_SCHEME = 'utf-8'
    # REQUIRED_PARAMETERS = 6


    try:

        inputFileName = input("Enter input file directory path with file name: ")
        opDirectory = input("Enter output directory path: ")
        dataType = input("Enter data type(JSON/XML): ")

        if "JSON" in dataType:
            url = 'https://www.lmsal.com/hek/her?cosec=2&&cmd=search&type=column'
            json=True
        elif "XML" in dataType:
            url = 'https://www.lmsal.com/hek/her?cosec=1&&cmd=search&type=column'
            xml=True

        with open(inputFileName, 'r') as f:
            contents = f.readlines()
            f.close()
        contents = [content.strip('\n') for content in contents]

        for token in contents:

            tokens = token.split(':')

            if 'Start Date' in tokens[0]:
                for tokenValue in tokens:
                    if '-' in tokenValue:
                        ymd = tokenValue.split('-')
                        startYear = ymd[0].strip()
                        startMonth = ymd[1].strip()
                        startDay = ymd[2].strip()

            elif 'End Date' in tokens[0]:

                for tokenValue in tokens:
                    if '-' in tokenValue:
                        ymd = tokenValue.split('-')
                        endYear = ymd[0].strip()
                        endMonth = ymd[1].strip()
                        endDay = ymd[2].strip()

            elif 'Start Time' in tokens[0]:
                for tokenValue in tokens:
                    if '-' in tokenValue:
                        hms = tokenValue.split('-')
                        startHour = hms[0].strip()
                        startMinute = hms[1].strip()
                        startSecond = hms[2].strip()

            elif 'End Time' in tokens[0]:
                for tokenValue in tokens:
                    if '-' in tokenValue:
                        hms = tokenValue.split('-')
                        endHour = hms[0].strip()
                        endMinute = hms[1].strip()
                        endSecond = hms[2].strip()

            elif 'Event Type' in tokens[0]:

                eventModule =[tokens[1].split(',')]
                eventModuleString = ",".join(eventModule[0]).strip()



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




    except Exception as e:
        print("Input Error: ", str(e))


    try:

        values = {'event_type': eventModuleString, 'event_region': EVENT_REGION, 'event_coordsys': coordinateValue,
                  'x1': x1Value, 'x2': x2Value,
                  'y1': y1Value, 'y2': y2Value, 'result_limit': RESULT_LIMIT,
                  'event_starttime': startYear +"-"+ startMonth +"-"+ startDay +"T"+ startHour +":"+startMinute+":"+ startSecond,
                  'event_endtime': endYear +"-"+ endMonth+"-"+ endDay +"T"+ endHour +":"+endMinute+":"+ endSecond}


        for i in range(0, len(filterCondition)):
            valuesLoop.append({'sparam' + str(i): filterCondition[i], 'op' + str(i): filterOperators[i],
                               'value' + str(i): filterConditionValue[i]})


        values1=values.copy()

        for i in range(0, len(valuesLoop)):
            values1.update(valuesLoop[i])

        print(values1)


        data = urllib.parse.urlencode(values1)
        data = data.encode(ENCODING_SCHEME)
        req = urllib.request.Request(url,data)
        resp = urllib.request.urlopen(req)
        resData = resp.read().decode('utf-8')


        if json:
            fileName = "'"+eventModuleString+"'"+"_event_startdate=" + startYear.strip() + "-" + startMonth.strip() + "-" + startDay.strip() + "T" +  startHour +"-"+startMinute+"-"+ startSecond + "_event_enddate=" + endYear.strip() + "-" + endMonth.strip() + "-" + endDay.strip() + "T" +endHour +"-"+endMinute+"-"+ endSecond+ ".json"
        elif xml:
            fileName = "'"+eventModuleString +"'"+"_event_startdate=" + startYear.strip() + "-" + startMonth.strip() + "-" + startDay.strip() + "T" + startHour + "-" + startMinute + "-" + startSecond + "_event_enddate=" + endYear.strip() + "-" + endMonth.strip() + "-" + endDay.strip() + "T" + endHour + "-" + endMinute + "-" + endSecond + ".xml"

        saveFile= open(opDirectory+fileName, 'w')
        saveFile.write(str(resData))
        saveFile.close()

    except Exception as e:
        print('Error:', str(e))


if __name__ == "__main__":
    main()
