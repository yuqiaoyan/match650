from lucene import *
from processString import *

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

class matcher:
#matcher will return professor results for a given student
	def __init__(self,index_dir="Tmp/preprocess_aff.index-dir"):
		self.dirPath = index_dir
		self.dir = SimpleFSDirectory(File(self.dirPath))
		self.analyzer = StandardAnalyzer(Version.LUCENE_35)
		self.searcher = IndexSearcher(self.dir)
		self.recentResult = []

	def getSearcher(self):
	#returns an IndexSearcher
		return self.searcher

	def reShingle(self,queryList,shingleSizeList):
	#processes each query in ueryList into shingleSizeList of shingles
	#returns a list of processed query strings
		processedQueryList = []
		for i,query in enumerate(queryList):
			if(shingleSizeList[i]==1): 
				processedQueryList.append(query) 
			else:
				processedQueryList.append(shingleQuery(query,shingleSizeList[i]))
		return processedQueryList
			

	def getQuery(self, student, fieldList):
	#REQ fields to be a string of fields seperated by comma in the student dictionary
	#returns a PyLucene query object to make a search against 

		#if we use processed_aff, then transform student affiliation to bigram
		if("processed_aff" in fieldList):
			student["processed_aff"] = shingleQuery(student["affiliation"],2)
		queryList = getQueryList(student,fieldList)
		print fieldList,queryList
		return (MultiFieldQueryParser(Version.LUCENE_35,fieldList,self.analyzer).parse(Version.LUCENE_35,queryList,fieldList,self.analyzer))


	def getProfMatch(self,student, numResults = 3, fieldList = ["interest","processed_aff"]):
	#student_profile is a dictionary with keys:
	#name, interest, affiliation 
		assert len(student["interest"].strip()) > 0, "Student must have an interest"		
		query = self.getQuery(student,fieldList)
		
		#get results from Index
		hits = self.searcher.search(query, numResults)

		#profList is a list of professor results
		profList = []


		for hit in hits.scoreDocs:
			doc = self.searcher.doc(hit.doc)
			profDict = {}
			profDict["name"] = doc.get("name")
			profDict["interest"] = doc.get("interest")
			profDict["affiliation"]=doc.get("affiliation")
			profList.append(profDict)
		
		#save the most recent list of results	
		self.recentResult = profList

		print "We found" + str(len(profList)) + "results"

		return profList

	def __str__(self):
		return 'Matcher Class \n[Index Directory: %s]' % (self.dirPath)

if __name__ == '__main__':
	#test code

	#create a fake student
	student = {}
	student['name'] = "Xu Ling"
	student['interest'] = "data mining, machine learning"
	student['affiliation'] = "university of michigan"
	student['processed_aff'] = "universityof ofmichigan"
	
	#create an instance of matcher
	a = matcher("Tmp/preprocess_aff.index-dir")
