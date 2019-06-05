import os
os.chdir('C:\\Users\\Administrator\\Desktop\\Argus\\Argus\\middleware\\training\\') # VM PATH

trainingPath = 'C:\\Users\\Administrator\\Desktop\\Argus\\Argus\\middleware\\training\\'
testingPath = 'C:\\Users\\Administrator\\Desktop\\Argus\\Argus\\middleware\\testing\\'


tempTraining = trainingPath+ 'file-1552992007498.txt'
tempTesting = testingPath + '20020329-1482.txt'
#tempTest = testingPath + doc2 

text_loaded = open(tempTesting, 'r').read()
text_loaded = text_loaded.replace("\n", "").strip()