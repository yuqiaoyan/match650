from lucene import *
initVM()
from indexing import initializeIndex
from customized_analyzer import BiGramShingleAnalyzer
import re

old_indexDir = "Tmp/affiliation.index-dir"
new_indexDir = "Tmp/preprocess_aff.index-dir.test"
shingle_pattern = r'\((.+?),.*?\)'
    
def copy_index(old_index_dir, new_index_dir):
    reader = IndexReader.open(SimpleFSDirectory(File(old_index_dir)))
    writer = initializeIndex(new_index_dir)
    # loop throught the docs in index
    for i in range(reader.maxDoc()):
        #get the doc by doc number
        print 'processing doc num', i
        doc = reader.document(i)
        #get the affiliation string
        affiliation = doc.get('affiliation')
        print 'processing affiliation,', affiliation

        shingle_list = rebuild_affiliation(affiliation)

        #add new field to the doc
        print 'shingle list is', shingle_list
        doc.add(Field('processed_aff', ' '.join(shingle_list),
            Field.Store.valueOf("YES"), Field.Index.valueOf("ANALYZED"),
            Field.TermVector.valueOf("WITH_POSITIONS")))
        writer.addDocument(doc)
    writer.commit()

def rebuild_affiliation(affiliation):
    shingle_list = []
    #get bi gram shingles with tokenStream
    shingles = BiGramShingleAnalyzer().tokenStream('f',
            StringReader(affiliation))

    #loop through the shingles
    while shingles.incrementToken():
        shingle = shingles.toString()
        print shingle
        """
        use regex to get the text in shingle 
        in this format 'term1 term2'
        """
        result = re.match(shingle_pattern, shingle)
        if result:
            #if matched, combine tow terms in the shingle to one term
            #then append it to the shingle_list
            print 'shingle is', "".join(result.group(1).split())
            shingle_list.append("".join(result.group(1).split()))
    return shingle_list

def initializeIndex(dir_name):
#returns an IndexWriter to build an index
	dir = SimpleFSDirectory(File(dir_name))
	analyzer = StandardAnalyzer(Version.LUCENE_35)
	return IndexWriter(dir, analyzer, True, IndexWriter.MaxFieldLength(512))	

if __name__ == "__main__":
    copy_index(old_indexDir, new_indexDir)
