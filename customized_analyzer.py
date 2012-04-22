from lucene import *
import lucene

class BiGramShingleAnalyzer(PythonAnalyzer):
    def __init__(self, outputUnigrams=False):
        PythonAnalyzer.__init__(self)
        self.outputUnigrams = outputUnigrams

    def tokenStream(self, field, reader):
        result = ShingleFilter(LowerCaseTokenizer(Version.LUCENE_35,reader))
        result.setOutputUnigrams(self.outputUnigrams)
        print 'result is', result
        return result
