import re
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

    count = 0
    for line in file:
        try:
            found = re.search('mnbdb(.+?)["["]', line).group(1)
            if "perl" in found:
                try:
                    found = 'perl SQL extension:' + re.search('2019:(.+?)#', line).group(1)

                except AttributeError:
                    found = 'Could not find String'
            else:
                found = re.search('mnb_live(.+?)["["]', line).group(1)

        except AttributeError:
            found = 'Could not find String'



        if found not in errorArr:
            errorArr.append(found)

        fullErrorArr.insert(count, found)

        count = count + 1

    count1 = 0
    for line3 in errorArr:
        errorCount.insert(count1, fullErrorArr.count(line3))
        count1 = count1 + 1

    #print(fullErrorArr)
    #print(errorCount)
    #print(errorArr)

    count2 = 0
    for line4 in errorArr:
        print(line4, '- has', errorCount[count2], 'occurrences')
        count2 += 1


    fileLength = file_len(filename)
    print('Total errors: ', fileLength)
file.close()
