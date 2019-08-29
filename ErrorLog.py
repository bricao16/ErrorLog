import re
import smtplib
from email.mime.text import MIMEText


#method to send email message if error occurs
def sendemail(error):
    smtp_server_name = 'smtp.gmail.com'
    port = '465' # for secure messages
    #port = '587'  # for normal messages
    sender = 'errormessages1@gmail.com'
    receiver = 'brian_cao@mnb.uscourts.gov'
    password = 'errors123'

    content = error
    msg = MIMEText(content)
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = 'Error Threshold Met'
    if port == '465':
        server = smtplib.SMTP_SSL('{}:{}'.format(smtp_server_name, port))
    else:
        server = smtplib.SMTP('{}:{}'.format(smtp_server_name, port))
        server.starttls() # this is for secure reason

    server.login(sender, password)
    server.send_message(msg)
    server.quit()

filename = 'C:/Users/bricao/PycharmProjects/live.txt'


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


with open(filename, "r") as file:

    fullErrorArr = []
    errorArr = []
    errorCount = []
    perlFlag = 0
    count = 0
    additionalErrorInfo = []
    finalError = []

    for line in file:
        try:
            found = re.search('mnbdb(.+?)["["]', line).group(1)
            if "perl" in found:
                perlFlag = 1
                try:
                    found = 'perl SQL extension:' + re.search('2019:(.+?)#', line).group(1)
                    found2 = found + re.search('failed.(.+$)', line).group(1)
                except AttributeError:
                    found = 'Could not find String'
            else:
                found = re.search('mnb_live(.+?)["["]', line).group(1)
                found2 = found + re.search(']:(.+$)', line).group(1)


        except AttributeError:
            found = 'Could not find String'

        #print(found2)
        try:
            if perlFlag == 0:
                found1 = re.search(']:(.+$)', line).group(1)
            else:
                found1 = re.search('failed.(.+$)', line).group(1)
        except AttributeError:
            found1 = 'Could not find String'

        if found1 not in additionalErrorInfo:
            additionalErrorInfo.append(found1)

        #print(found1)
        if found not in errorArr:
            errorArr.append(found)

        if found2 not in finalError:
            finalError.append(found2)

        fullErrorArr.insert(count, found)

        count = count + 1

    c = 0
    for x in finalError:
        print(finalError[c])
        c += 1
    count4 = 0
    #for line6 in additionalErrorInfo:
       # additionalErrorInfo.insert(count4, fullErrorArr.count(line6))
       # count4 = count4 + 1


    count1 = 0
    for line3 in errorArr:
        errorCount.insert(count1, fullErrorArr.count(line3))
        count1 = count1 + 1

    #print(fullErrorArr)
    #print(errorCount)
    #print(errorArr)

    count2 = 0
    fullemail = ''
    for line4 in errorArr:
        email = str(line4) + str(' - has ') + str(errorCount[count2]) + str(' occurrences')
       # print(email)
        if errorCount[count2] >= 5:
            fullemail = str(fullemail) + str('\n') + str(email) + str('\n')
        count2 += 1
        fileLength = file_len(filename)

    count5 = 0
    for line5 in finalError:
        for line6 in errorArr:
            if errorArr[count5] in finalError[count5]:
                
        count5 += 1
    #print(fullemail)
    if fullemail != "":
        #sendemail(str(fullemail))
        print('sent email')

    print('Total errors: ', fileLength)
file.close()
