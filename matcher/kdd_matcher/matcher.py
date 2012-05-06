from lucene import *
from processString import *
import re
import string

scorePattern = re.compile("^[0-9]+[.][0-9]+")
fieldScorePattern = re.compile(r'\n\s\s[0-9]+[.][0-9]+') 
fieldMatchPattern = re.compile(r'[a-z_]+:[a-z]+') 


def isOneWord(aString):
#returns true if aString has only one word
	return(len(aString.split(" "))==1)

def getFieldExplainList(explain):
#for each field a student matches the professor
#get the field score, field matched items, and field name in a list

	#get the subscore, and matched items for each field as a list
	fieldScoreList = fieldScorePattern.findall(explain)
	fieldMatchList = fieldMatchPattern.findall(explain)
	index = -1
	currField = ""
	fieldExplainList = [{} for i in range(0,len(fieldScoreList))]

	#if we found matched items for at least one field
	if(len(fieldMatchList) > 0):
		for fieldMatch in fieldMatchList:
			fieldName,match = fieldMatch.split(':')
			if(currField != fieldName):
				index += 1
				currField = fieldName
				fieldExplainList[index]['score'] = fieldScoreList[index][4:]
			try:
				fieldExplainList[index]['name']=fieldName
				if 'matchedItems' in fieldExplainList[index]:
					if string.find(fieldExplainList[index]['matchedItems'],match) >= 0:
						continue
				fieldExplainList[index]['matchedItems'] = fieldExplainList[index].setdefault('matchedItems',"")+match
			except:
				raise
				#print "index is", index
				#print "field name", fieldName
	return fieldExplainList

def getScore(explain):
#returns the Lucene score for the given result
#score is returned as a float
	score = -1
	if(scorePattern.findall(explain) > 0):
		score = scorePattern.findall(explain)[0]
	return(float(score))

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
		self.recentQuery = None

	def explainPos(self,pos):
	#requires a position that's one or greater and less than the recentResult
	#returns a tuple: Lucene score, fieldExplainList of
	#dict with keys: "matchedItems", "score", "name" - all strings

		if( pos < 1 or pos > len(self.recentResult)):
			print "Please pick a position with results"
		else:
			index = pos-1
			explanation = self.searcher.explain(self.recentQuery,self.recentResult[index]['id'])
			explainString = explanation.toString()
			
			#if there is an explanation
			if(len(explainString) > 0):

			#get the overall score of the result and
			#get summary data on each field as a list
				score = getScore(explainString)
				print "score is ",score
				fieldExplainList = getFieldExplainList(explainString)
				print "field summary is ", fieldExplainList
			return score,fieldExplainList

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

	def validateArguments(self,student,fieldList):
	#student must have an interest field, processed_aff must be a bigram
	#if processed_aff only has one word, then update fieldList to include
	#affiliation only and return fieldList 
		assert len(student["interest"].strip()) > 2, "Student must have an interest"		

		if "processed_aff" in fieldList:
			if(len(student["affiliation"].strip()) == 0):
				fieldList.remove("processed_aff")
			elif(isOneWord(student["affiliation"])):
				fieldList.remove("processed_aff")
				fieldList.append("affiliation")
			print "fieldList is", fieldList
		return fieldList

	def getProfMatch(self,student, numResults = 3, fieldList = ["interest","processed_aff"]):
	#student_profile is a dictionary with keys:
	#name, interest, affiliation 

		fieldList = self.validateArguments(student,fieldList)

		query = self.getQuery(student,fieldList)
		self.recentQuery = query		

		#get results from Index
		hits = self.searcher.search(query, numResults)

		#profList is a list of professor results
		profList = []


		for hit in hits.scoreDocs:
			doc = self.searcher.doc(hit.doc)
			profDict = {}
			profDict["id"] = hit.doc
			profDict["name"] = doc.get("name")
			profDict["interest"] = doc.get("interest")
			profDict["affiliation"]=doc.get("affiliation")
			profDict["processed_aff"]=doc.get("processed_aff")
			profList.append(profDict)
		
		#save the most recent list of results	
		self.recentResult = profList

		print "We found" + str(len(profList)) + "results"

		return profList

	def __str__(self):
		return 'Matcher Class \n[Index Directory: %s]' % (self.dirPath)

def generateTestStudent():
	#test code

	#create a fake student
	student = {}
	student['name'] = "Xu Ling"
	student['interest'] = "support vector machine"
	student['affiliation'] = "  "
	student['processed_aff'] = ""

	return student	
