__author__ = 'quasim0do'

import os
import PythonROUGE
import csv

scores = {}
counter = 0
for i in range(1, 13):
    for j in range(1, 10):
        d = 'raw/output/' + str(i) + '.' + str(j) + '/'
        if os.path.exists(d):
            for k in range(1, 32):
                if os.path.exists(d + str(k)):
                    modelSummaryList = []
                    model = [d + 'Model' + str(i) + '.' + str(j)]
                    guessSummary = [d + str(k)]
                    recall, precision, F_measure = PythonROUGE.PythonROUGE(guessSummary, [model], ngram_order=1)
                    scores[str(counter)] = dict()
                    scores[str(counter)]['recall'] = recall
                    scores[str(counter)]['precision'] = precision
                    scores[str(counter)]['F_measure'] = F_measure
                    counter += 1
# recall, precision, F_measure = PythonROUGE.PythonROUGE(['raw/output/1.2/10'], [['raw/output/1.2/Model1.2']], ngram_order=1)
# print(recall[0], precision[0], F_measure[0])
# Let us just collect the gold standard scores as well
goldScore = []
total = 0
for i in range(1, 13):
    for j in range(1, 10):
        d = 'scores/' + str(i) + '.' + str(j) + '/'
        if os.path.exists(d):
            with open(d + 'ave', 'r') as f:
                for line in f:
                    goldScore.append(line)
                    total += 1
            # scoreFile = open(d + 'ave', 'r')
            # lines = scoreFile.readlines()
            # scoreFile.close()
            #for l in lines:

fileName = open('Rouge_scores', 'wb')
writer = csv.writer(fileName, quoting=csv.QUOTE_NONE)
writer.writerow(('Recall', 'Precision', 'F-measure', 'Gold Std marks'))
for i in range(total):
    temp = float(goldScore[i]) # to remove the quotes
    writer.writerow([scores[str(i)]['recall'][0], scores[str(i)]['precision'][0], scores[str(i)]['F_measure'][0], temp])

