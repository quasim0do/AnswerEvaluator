from __future__ import division

__author__ = 'quasim0do'



import numpy as np
from pylab import scatter, show, legend, xlabel, ylabel
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from sklearn import svm

#data visualizing method
def visualize(X, y):
    '''Makes a 3D visual scatterplot of the input data.

    X is the feature matrix and y is the label vector.'''
    scaledX = X

    pos = np.where(y > 3)
    neg = np.where(y <=3)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(scaledX[pos, 0], scaledX[pos, 1], scaledX[pos, 2], marker='o', c='b')
    ax.scatter(scaledX[neg, 0], scaledX[neg, 1], scaledX[neg, 2], marker='x', c='r')

    ax.set_xlabel('Recall')
    ax.set_ylabel('Precision')
    ax.set_zlabel('F-score')

    legend(['Incorrect', 'Correct'])

    show()


#loading the dataset
data = np.genfromtxt('Rouge_scores', delimiter=',', skip_header=True)

X = data[:, 0:3]
y = data[:, 3]


#Method to visualize the data. Uncomment to activate
#visualize(X, y)


#let us convert y to a binary form.
pos = np.where (y > 3.5)
neg = np.where (y <= 3.5)
binaryY = np.ones(y.shape)
binaryY[neg] = 0

XTrain = X[:-400, :]
yTrain = binaryY[:-400] #data for training the classifier. It takes the entire batch except the last 400 rows

Xcv = X[-400:, :]
ycv = binaryY[-400:] #data for cross-validation. It takes the last 400 rows which our classifier hasn't "seen" yet.

#Let us create vectors for the various imput parameters that we need to provide to the SVM. Let's have a range of values.

cVec = [0.01, 0.03, 0.1, 0.3, 10, 30, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200]
sigmaVec = [0.01, 0.03, 0.1, 0.3, 10, 30, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200]
optimumF_score = 0
optimumPrecision = 0
optimumRecall = 0
optimumC = 0
optimumSigma = 0
for c in cVec:
    for sigma in sigmaVec:
        classifier = svm.SVC(gamma=sigma, C=c)
        classifier.fit(XTrain, yTrain)
        #Now we have trained our algorithm. Let's get some metric from our cross-validation data.
        hypothesis = classifier.predict(Xcv)
        #let us get some key parameters. The comparison between ycv and the hypothesis is stored in a vector using the following legend ;
        #1 for True Positives.
        #2 for False Positives.
        #3 for True Negatives.
        #4 for False Negatives.
        #print "Ycv {0}".format(ycv)
        #print "Hypothesis {0}".format(hypothesis)
        paraVector = np.zeros(ycv.shape)
        r = ycv.shape
        for i in range(r[0]):
            if (hypothesis[i] == 1 and ycv[i] == 1):
                paraVector[i] = 1
            elif (hypothesis[i] == 1 and ycv[i] == 0):
                paraVector[i] = 2
            elif (hypothesis[i] == 0 and ycv[i] == 1):
                paraVector[i] = 3
            elif (hypothesis[i] == 0 and ycv[i] == 0):
                paraVector[i] = 4
        TP = (paraVector == 1).sum()
        FP = (paraVector == 2).sum()
        TN = (paraVector == 3).sum()
        FN = (paraVector == 4).sum()
        precision = TP / (TP + FP)
        recall = TP / (TP + TN)
        #print (TP, FP, TN, FN, precision, recall)
        if (precision + recall != 0):
            F_score = (2 * precision * recall) / (precision + recall)
        else:
            F_score = 0
        if F_score >  optimumF_score:
            optimumF_score = F_score
            optimumPrecision = precision
            optimumRecall = recall
            optimumC = c
            optimumSigma = sigma
print 'The best F_score was found to be {0} with a precision of {1} and a recall of {2} and C={3} and Sigma={4}'.format(optimumF_score, optimumPrecision, optimumRecall, optimumC, optimumSigma)