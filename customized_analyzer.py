from lucene import *
import lucene

class BiGramShingleAnalyzer(PythonAnalyzer):
    def __init__(self, outputUnigrams=False):
        PythonAnalyzer.__init__(self)
        self.outputUnigrams = outputUnigrams

    def tokenStream(self, field, reader):
        result = ShingleFilter(LowerCaseTokenizer(Version.LUCENE_35,reader))
        #result = LowerCaseTokenizer(Version.LUCENE_35,reader)
        result.setOutputUnigrams(self.outputUnigrams)
        print 'result is'
        return result

class MyTokenStream(lucene.PythonTokenStream):
    def __init__(self, terms):
        lucene.PythonTokenStream.__init__(self)
        self.terms = iter(terms)
        self.addAttribute(lucene.TermAttribute.class_)
    def incrementToken(self):
        for term in self.terms:
            self.getAttribute(lucene.TermAttribute.class_).setTermBuffer(term)
            return True
        return False

