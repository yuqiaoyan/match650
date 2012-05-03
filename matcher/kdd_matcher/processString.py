import re
from lucene import *

shingle_pattern = r'\((.+?),.*?\)'

def tokenStream(reader,shingleSize):
                result = ShingleFilter(LowerCaseTokenizer(Version.LUCENE_35,reader),shingleSize,shingleSize)
                result.setOutputUnigrams(False)
                return result

def shingleQuery(query,shingleSize):
#processes the query into a string of shingleSize shingles
#returns a string

    shingle_list = []
    #get bi gram shingles with tokenStream
    shingles = tokenStream(StringReader(query),shingleSize)

    #loop through the shingles
    while shingles.incrementToken():
        shingle = shingles.toString()
        """
        use regex to get the text in shingle 
        in this format 'term1 term2'
        """
        result = re.match(shingle_pattern, shingle)
        if result:
            #if matched, combine tow terms in the shingle to one term
            #then append it to the shingle_list
            shingle_list.append("".join(result.group(1).split()))
    return " ".join(shingle_list)
