import sys
import csv
import os
import lucene
from lucene import *
#INDEX_DIR = "Tmp/REMOVEME.index-dir"
INDEX_DIR = "Tmp/affiliation.index-dir"
STUDENT_PATH = "getData/student_data/"
MAX = 10

def explain_score(searcher, docID, query):
#returns the explanation object for a given
#query (student), docID(professor)
    explanation = searcher.explain(query, docID)
    print "Explanation Dump: "
    print explanation.toString()
    return explanation

def initial_searcher():
    lucene.initVM()
    indexDir = INDEX_DIR 
    dir = SimpleFSDirectory(File(indexDir))
    analyzer = StandardAnalyzer(Version.LUCENE_30)
    searcher = IndexSearcher(dir)
    return searcher, analyzer

def getQueryList(student,fieldList):
#fieldList is list of fields we want to use for scoring
#student is dictionary of student_profile info
#REQUIRES: student_profile must have interest and affiliation information
#EFF: returns a MultiFieldQuery object
    queryList = []
    for field in fieldList:
        fieldValue = ""
        if (student.get(field)):
            fieldValue = student[field]
        queryList.append(fieldValue)
    return queryList

def search_by_student(student, analyzer, searcher,fieldList):
    queries = getQueryList(student,fieldList) 
    query = MultiFieldQueryParser(Version.LUCENE_35,fieldList,analyzer).parse(Version.LUCENE_35,queries,fieldList,analyzer)
    hits = searcher.search(query, MAX)
    #explanationOutput = ""

    for hit in hits.scoreDocs:
        print hit.score 
        doc = searcher.doc(hit.doc)
        print doc.get("name")
        print doc.get("interest")
        print doc.get("affiliation")
        print '...................'
        print '...................'
        #explanation = explain_score(searcher,hit.doc,query)
        #explanationOutput += explanation.toHtml()

	#print "this is the hits.scoreDocs..."
	#print hits.scoreDocs
    #write the explanation for the scores
    #outputFile = open("explanation.html","w")   
    #outputFile.write(explanationOutput)

if __name__ == "__main__":
    searcher, analyzer = initial_searcher()
    file_list = os.listdir(STUDENT_PATH)
    fieldList = sys.argv[1:]

    for f in os.listdir(STUDENT_PATH):
        print 'opening', STUDENT_PATH + f
        reader = csv.reader(open(STUDENT_PATH + f, 'r'), delimiter=',', quotechar='"')
        for line in reader:
            print line
            student_profile = {}
            student_profile['name'] = line[0]
            student_profile['interest'] = line[1]
            student_profile['affiliation'] = line[2]
            print 'searching', student_profile['name']
            print 'interests are' , student_profile['interest']
            print 'affiliation is' , student_profile['affiliation']
            print '.......'
            print 'result is:'
            search_by_student(student_profile, analyzer, searcher,fieldList)
            print '___________________________'
            print '___________________________'
            print '___________________________'

    

