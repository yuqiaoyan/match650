from lucene import *
import lucene


def myShingle(aString):
#example: univ of michigan
#output: univof ofmichigan
	result = ""
	if(aString):
		wordList = aString.replace(",","").split(" ")
		for i in range(0,len(wordList)-1):
			result += wordList[i] + wordList[i+1]
			result += " "
	return result

class BiGramShingleAnalyzer(PythonAnalyzer):
    def __init__(self, outputUnigrams=False):
        PythonAnalyzer.__init__(self)
        self.outputUnigrams = outputUnigrams

    def tokenStream(self, field, reader):
        result = ShingleFilter(LowerCaseTokenizer(Version.LUCENE_35,reader))
        result.setOutputUnigrams(self.outputUnigrams)
        print 'result is', result
        return result
