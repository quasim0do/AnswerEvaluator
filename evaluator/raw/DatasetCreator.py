__author__ = 'quasim0do'

import os
import re
allAnswers = []
for i in range(1, 13):
    for j in range(1, 11):
        fileName = str(i) + '.' + str(j)
        if os.path.exists(fileName):
            textFile = open(fileName, 'r')
            lines = textFile.readlines()
            textFile.close()
            count = 1
            for l in lines:
                d = 'output/'+ str(i) + '.' + str(j)
                fileName = d + '/' + str(count)
                if not os.path.exists(d):
                    os.makedirs(d, 0o777)
                opFile = open(fileName, 'w')
                sequencesNoise = [str(i) + '.' + str(j), '<br><br>', '<br>'] #get rid of the sequence numbers and other unwanted sequences
                for s in sequencesNoise:
                    l = l.replace(s, '')
                opFile.write(l)
                count += 1
                opFile.close()

#Now let us take the model summaries
fileName = 'answers'
ansFile = open(fileName, 'r')
lines = ansFile.readlines()
ansFile.close()
for l in lines:
        #l = re.sub('^[0-9]* . [0-9]*]', '', l)
        lineArray = l.split(' ')
        dName = lineArray[0]
        lineArray.pop(0)
        l = ' '.join(lineArray)
        fileName = 'output/' + dName + '/Model' + dName
        opFile = open(fileName, 'w')
        opFile.write(l)
        opFile.close()