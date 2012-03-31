import lucene
from lucene import \
    SimpleFSDirectory, System, File, \
    Document, Field, StandardAnalyzer, IndexWriter, Version
    
################### GLOBALS AND CONFIGURATIONS #####################################
#interests is configured to break up into tokens but keep the position offsets so we can search for phrase
#name is configured simply to store all the entirey of the string
 
configs = {'interest': ["YES","ANALYZED","WITH_POSITIONS"],\
			'name': ["YES","NOT_ANALYZED","NO"],\
			'affiliation':["YES","ANALYZED","WITH_POSITIONS"]}



####################################################################################
    
def addDoc(indexWriter, profile):
#profile is a dictionary of a professor's profile
#[name]['Eytan Adar']
#[affiliation]['univ of michigan']
	doc = Document()
	for key, value in profile.items():
		config_t = configs[key]
		doc.add(Field(key,value, Field.Store.valueOf(config_t[0]),Field.Index.valueOf(config_t[1]),Field.TermVector.valueOf(config_t[2])))
		indexWriter.addDocument(doc)

def initializeIndex():
#returns an IndexWriter to build an index
	lucene.initVM()
	indexDir = "/Tmp/REMOVEME.index-dir"
	dir = SimpleFSDirectory(File(indexDir))
	analyzer = StandardAnalyzer(Version.LUCENE_35)
	return(IndexWriter(dir, analyzer, True, IndexWriter.MaxFieldLength(512)))
	
#test = [{'name': 'Eytan Adar', 'interest': "blah"}, {'name': 'foo', 'interest': 'foobars'}]

#buildIndex(test)