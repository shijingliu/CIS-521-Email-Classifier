# Modified from code by Andrew McCallum of UMass Amherst

# Your job is to replace the two sections marked below with code and
# run the classifier on test files.

import math
import sys
import glob
import pickle
from collections import defaultdict

# In the documentation and variable names below "class" is the same
# as "category"

def naivebayes (dirs):
    """Train and return a naive Bayes classifier.  
    The datastructure returned is an array of tuples, one tuple per
    class; each tuple contains the class name (same as dir name)
    and the multinomial distribution over words associated with
    the class"""
    # Set up the vocabulary for all files in the training set
    vocab = defaultdict(int)
    for dir in dirs:
        vocab.update(files2countdict(glob.glob(dir+"/*")))
    # Set all counts to 0
    vocab = defaultdict(int, zip(vocab.iterkeys(), [0 for i in vocab.values()]))
    classes = []
    for dir in dirs:
        # Initialize to zero counts
        countdict = defaultdict(int, vocab)
        # Add in counts from this class
        countdict.update(files2countdict(glob.glob(dir+"/*")))
        #***
        # Here turn the "countdict" dictionary of word counts into
        # into a dictionary of smoothed word probabilities   
        #***  
        getTuple = countdict.items()
        
        #obtain the total number of items in the training pool 
        totalnumber = 0
        for j in getTuple:
            totalnumber += j[1]
    
        #convert dict to tuple so as to calculate the probability
        for i in getTuple:
            temp = i[:-1]+((i[1]+1)/(totalnumber + len(getTuple)), )
            i = temp

        #get tuple back to defaultdict format 
        getdictback = defaultdict (int)
        for k in getTuple:
            getdictback[k[0]] = k[1]
        classes.append((dir,getdictback))  
    return classes  


def classify (classes, filename):
    """Given a trained naive Bayes classifier returned by naivebayes(), and
    the filename of a test document, d, return an array of tuples, each
    containing a class label; the array is sorted by log-probability
    of the class, log p(c|d)"""   
    answers = []
    print 'Classifying', filename  
    for c in classes:
        extractwords = c[1]
        score = 0
        
        #obtain the total number of items in the training pool 
        oldtuple = c[1].items()
        totalnumber = 0
        for j in oldtuple:
            totalnumber += j[1]  

        #obtain the test file words
        testfile = defaultdict(int)
        for word in open(filename).read().split():
            lowerword = word.lower()
            if(eliminateNoneWord(lowerword)):
                testfile[word.lower()] += 1
    
        getTuple = testfile.items()
        for k in getTuple:
            if extractwords[k[0]] == 0:
                score += math.log(1.0/(totalnumber + len(c[1])))
            else:
                score += math.log(extractwords[k[0]])  
        #***   
        # Here, compute the naive bayes score for a file for a given class by:  
        # 1. Reading in each word, and converting it to lower case (see code below)
        # 2. Adding  the log probability of that word for that class
        #*** 
        
        answers.append((score,c[0]))
    answers.sort()
    return answers


def files2countdict (files):
    """Given an array of filenames, return a dictionary with keys
    being the space-separated, lower-cased words, and the values being
    the number of times that word occurred in the files."""
    d = defaultdict(int)
    for file in files:
        
        for word in open(file).read().split():
            lowerword = word.lower()
            if(eliminateNoneWord(lowerword)):
                d[word.lower()] += 1
    return d


#=======================================
#elminate all the useless information to obtain the final
#information   
#=======================================
def eliminateNoneWord(textwords):
    if ('=' in textwords) or ('<' in textwords) or (':' in textwords) or ('>' in textwords):
        return False
    elif ('-' in textwords) or ('.' in textwords) or ('*' in textwords) or ('_' in textwords):
        return False
    elif (')' in textwords) or ('(' in textwords) or ('/' in textwords) or ('+' in textwords):
        return False
    elif ('?' in textwords) or (',' in textwords) or ('@' in textwords) or ('|' in textwords):
        return False
    elif ('#' in textwords) or ('!' in textwords) or ('%' in textwords) or ('^' in textwords):
        return False
    elif ('$' in textwords) or ('&' in textwords) or ('*' in textwords) or ('[' in textwords):
        return False
    elif (']' in textwords) or ('{' in textwords) or ('}' in textwords) or ('~' in textwords):
        return False
    elif textwords.isdigit():
        return False
    elif ('1' in textwords) or ('2' in textwords) or ('3' in textwords) or ('4' in textwords) or ('5' in textwords) or ('6' in textwords) or ('7' in textwords) or ('8' in textwords) or ('9' in textwords):
        return False
    else:
        return True


#==========================================
#this is just for problem 5 and problem 6
#the program go through the entire directory
#rather than each file every time     
#==========================================
def testSpamErrorRate (classes, dir):
    countSpam = 0
    files = glob.glob(dir+"/*")
    for file in files:
        print 'Classifying', file
        answers = []
        for c in classes:
            extractwords = c[1]
            score = 0
            
            #obtain the total number of items in the training pool
            oldtuple = c[1].items()
            totalnumber = 0
            for j in oldtuple:
                totalnumber += j[1]  

            #obtain the test file words
            testfile = defaultdict(int)
            for word in open(file).read().split():
                lowerword = word.lower()
                if(eliminateNoneWord(lowerword)):
                    testfile[word.lower()] += 1
        
            getTuple = testfile.items()
            for k in getTuple:
                if extractwords[k[0]] == 0:
                    score += math.log(1.0/(totalnumber + len(c[1])))
                else:
                    score += math.log(extractwords[k[0]])  
            
            answers.append((score,c[0]))
        answers.sort()
        print answers[1]
        if answers[1][1] == 'C:\\Users\\shijingliu\\Dropbox\\All the courses at Penn\\CIS 521\\Tree Augmented Naive Bayes\\Naive Bayes\\spamham\\spamham\\spam':
            countSpam += 1
    print "the spam error rate is:"
    print 1-countSpam*1.0/1390


#====================================
#this is just for testing ham error rate 
#====================================
def testHamErrorRate (classes, dir):
    countHam = 0
    files = glob.glob(dir+"/*")
    for file in files:
        print 'Classifying', file
        answers = []
        for c in classes:
            extractwords = c[1]
            score = 0
            
            #obtain the total number of items in the training pool
            oldtuple = c[1].items()
            totalnumber = 0
            for j in oldtuple:
                totalnumber += j[1]  

            #obtain the test file words
            testfile = defaultdict(int)
            for word in open(file).read().split():
                lowerword = word.lower()
                if(eliminateNoneWord(lowerword)):
                    testfile[word.lower()] += 1
        
            getTuple = testfile.items()
            for k in getTuple:
                if extractwords[k[0]] == 0:
                    score += math.log(1.0/(totalnumber + len(c[1])))
                else:
                    score += math.log(extractwords[k[0]])  
            
            answers.append((score,c[0]))
        answers.sort()
        print answers[1]
        if answers[1][1] == 'C:\\Users\\shijingliu\\Dropbox\\All the courses at Penn\\CIS 521\\Tree Augmented Naive Bayes\\Naive Bayes\\spamham\\spamham\\ham':
            countHam += 1
    print "the ham error rate is:"
    print 1-countHam*1.0/1390   

#==================================
#just for testing test pool 
#==================================
def testTestPool (classes, dir):
    files = glob.glob(dir+"/*")
    for file in files:
        print 'Classifying', file
        answers = []
        for c in classes:
            extractwords = c[1]
            score = 0
            
            #obtain the total number of items in the training pool
            oldtuple = c[1].items()
            totalnumber = 0
            for j in oldtuple:
                totalnumber += j[1]  

            #obtain the test file words
            testfile = defaultdict(int)
            for word in open(file).read().split():
                lowerword = word.lower()
                if(eliminateNoneWord(lowerword)):
                    testfile[word.lower()] += 1
        
            getTuple = testfile.items()
            for k in getTuple:
                if extractwords[k[0]] == 0:
                    score += math.log(1.0/(totalnumber + len(c[1])))
                else:
                    score += math.log(extractwords[k[0]])  
            
            answers.append((score,c[0]))
        answers.sort()
        print answers[1]
   



#=============================
#not using this part in my program 
#=============================
'''
if __name__ == '__main__':
    print 'argv', sys.argv
    print "Usage:", sys.argv[0], "classdir1 classdir2 [classdir3...] testfile"
    dirs = sys.argv[1:-1]
    testfile = sys.argv[-1]
    nb = naivebayes (dirs)
    print classify(nb, testfile)
    pickle.dump(nb, open("classifier.pickle",'w'))
'''
   
