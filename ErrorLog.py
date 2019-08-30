import re
import smtplib
from email.mime.text import MIMEText


# method to send email message if error occurs
def sendemail(error):
    smtp_server_name = 'smtp.gmail.com'
    port = '465'  # for secure messages
    # port = '587'  # for normal messages
    sender = 'errormessages1@gmail.com'
    password = 'errors123'

    #Change to receiving email
    receiver = 'brian_cao@mnb.uscourts.gov'

    content = error
    msg = MIMEText(content)
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = 'Error Threshold Met'
    if port == '465':
        server = smtplib.SMTP_SSL('{}:{}'.format(smtp_server_name, port))
    else:
        server = smtplib.SMTP('{}:{}'.format(smtp_server_name, port))
        server.starttls()  # this is for secure reason

    server.login(sender, password)
    server.send_message(msg)
    server.quit()

#Change to error file path
filename = 'C:/Users/bricao/PycharmProjects/ErrorLog/live.txt'

#function to get how many lines the error file has
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

    #loop that parses each line for the error messages
    for line in file:
        #see if error line is from perl SQL extension
        try:
            ErrorFound = re.search('mnbdb(.+?)["["]', line).group(1)
            #check if perl is in the error
            if "perl" in ErrorFound:
                perlFlag = 1
                try:
                    #error type with line number
                    ErrorFound = 'perl SQL extension:' + re.search('2019:(.+?)#', line).group(1)
                    #extra error info on line
                    ExtraErrorFound = ErrorFound + re.search('failed.(.+$)', line).group(1)
                except AttributeError:
                    ErrorFound = 'Could not find String'
            #if perl not in line
            else:
                ErrorFound = re.search('mnb_live(.+?)["["]', line).group(1)
                ExtraErrorFound = ErrorFound + re.search(']:(.+$)', line).group(1)

        except AttributeError:
            ErrorFound = 'Could not find String'
        # print(found2)

        try:
            #storing extra error info
            if perlFlag == 0:
                found1 = re.search(']:(.+$)', line).group(1)
            else:
                found1 = re.search('failed.(.+$)', line).group(1)
        except AttributeError:
            found1 = 'Could not find String'

        #storing additional error info into array
        if found1 not in additionalErrorInfo:
            additionalErrorInfo.append(found1)
            #print(found1)

        #storing each unique error in errorArr array
        if ErrorFound not in errorArr:
            errorArr.append(ErrorFound)

        if ExtraErrorFound not in finalError:
            finalError.append(ExtraErrorFound)

        #creating array with all lines
        fullErrorArr.insert(count, ErrorFound)

        count = count + 1
        #resetting perlFlag
        perlFlag = 0

    count1 = 0
    for line3 in errorArr:
        errorCount.insert(count1, fullErrorArr.count(line3))
        count1 = count1 + 1

    eCount = 0
    for i in errorArr:
        print(errorArr[eCount])
        eCount += 1

    count2 = 0
    fullemail = ''
    for line4 in errorArr:
        #email string
        email = str(line4) + str(' - has ') + str(errorCount[count2]) + str(' occurrences')
        # print(email)
        #filtering errors to only email the errors that occur more than  5 times
        if errorCount[count2] >= 5:
            fullemail = str(fullemail) + str('\n') + str(email) + str('\n')
        count2 += 1
        fileLength = file_len(filename)

    if fullemail != "":
        sendemail(str(fullemail))

    print('Total errors: ', fileLength)
file.close()
