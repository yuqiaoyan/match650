import sys
import csv
import os
import lucene
from lucene import \
            SimpleFSDirectory, System, File, \
                Document, Field, StandardAnalyzer, \
                IndexSearcher, Version, QueryParser
INDEX_DIR = "Tmp/REMOVEME.index-dir"
STUDENT_PATH = "getData/student_data/"
MAX = 10

def initial_searcher():
    lucene.initVM()
    indexDir = INDEX_DIR 
    dir = SimpleFSDirectory(File(indexDir))
    analyzer = StandardAnalyzer(Version.LUCENE_30)
    searcher = IndexSearcher(dir)
    return searcher, analyzer

def search_by_student(student, analyzer, searcher):
    query = QueryParser(Version.LUCENE_35, 'interest', analyzer).parse(student['interest'])
    hits = searcher.search(query, MAX)

    for hit in hits.scoreDocs:
        print hit.score 
        doc = searcher.doc(hit.doc)
        print doc.get("name").encode("utf-8")
        print doc.get("interest").encode("utf-8")

if __name__ == "__main__":
    searcher, analyzer = initial_searcher()
    file_list = os.listdir(STUDENT_PATH)
    for f in os.listdir(STUDENT_PATH):
        print 'opening', STUDENT_PATH + f
        reader = csv.reader(open(STUDENT_PATH + f, 'r'), delimiter=',', quotechar='\"')
        for line in reader:
            student_profile = {}
            student_profile['name'] = line[0]
            student_profile['interest'] = line[1]
            print 'searching', student_profile['name']
            print 'interests are' , student_profile['interest']
            print '.......'
            print 'result is:'
            search_by_student(student_profile, analyzer, searcher)

