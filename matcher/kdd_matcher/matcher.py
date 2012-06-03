from lucene import *
from processString import *
import os
import re
import string

scorePattern = re.compile("^[0-9]+[.][0-9]+")
#fieldScorePattern = re.compile(r'\n\s\s[0-9]+[.][0-9]+') 
fieldMatchPattern = re.compile(r'[a-z_]+:[a-z]+') 
default_index_dir = os.path.join(os.path.abspath(os.path.join(os.path.abspath(__file__), os.path.pardir)),'Tmp/preprocess_aff.index-dir') 

def isOneWord(aString):
#returns true if aString has only one word
	return(len(aString.split(" "))==1)

def getFieldExplainList(explain,fieldList):
#for each field a student matches the professor from the explain test
#get the field matched items, and field name in a list
#return a LIST of dictionary by keys: name and matchedItems of strings

	#get the subscore, and matched items for each field as a list
	#fieldScoreList = fieldScorePattern.findall(explain)
	fieldMatchList = fieldMatchPattern.findall(explain)
	index = -1
	currField = ""
	fieldExplainList = [{} for i in range(0,len(fieldList))]

	#if we found matched items for at least one field
	if(len(fieldMatchList) > 0):
		for fieldMatch in fieldMatchList:
			fieldName,match = fieldMatch.split(':')
			if(currField != fieldName):
				index += 1
				currField = fieldName
				#fieldExplainList[index]['score'] = fieldScoreList[index][3:]
			try:
				fieldExplainList[index]['name']=fieldName
				if 'matchedItems' in fieldExplainList[index]:
					if string.find(fieldExplainList[index]['matchedItems'],match) >= 0:
						continue
				try:
					fieldExplainList[index]['matchedItems']+= ", " + match
				except:
					fieldExplainList[index]['matchedItems'] = match
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
	def __init__(self,index_dir=default_index_dir):
		self.dirPath = index_dir
		self.dir = SimpleFSDirectory(File(self.dirPath))
		self.analyzer = StandardAnalyzer(Version.LUCENE_35)
		self.searcher = IndexSearcher(self.dir)
		self.recentResult = []
		self.recentQuery = None
		self.fieldList = None

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
				fieldExplainList = getFieldExplainList(explainString,self.fieldList)
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
			

	def getQuery(self, student, fieldList,boosts):
	#REQ fields to be a string of fields seperated by comma in the student dictionary
	#returns a PyLucene query object to make a search against 

		#if we use processed_aff, then transform student affiliation to bigram
		if("processed_aff" in fieldList):
			student["processed_aff"] = shingleQuery(student["affiliation"],2)
		queryList = getQueryList(student,fieldList)
		print fieldList,queryList

		if boosts:
				print "we are boosting"
				#Lucene requires a Map class,copy boosts as a boostMap
				boostMap = HashMap()
				for key in boosts.keys():
						boostMap.put(key,boosts[key])
			
				query = MultiFieldQueryParser(Version.LUCENE_35,fieldList,self.analyzer,boostMap).parse(Version.LUCENE_35,queryList,fieldList,self.analyzer)
		else:
				query = MultiFieldQueryParser(Version.LUCENE_35,fieldList,self.analyzer).parse(Version.LUCENE_35,queryList,fieldList,self.analyzer)

		return query

	def updateArguments(self,student,fieldList,boosts):
	#if student has no affiliation information, then do not use affiliation in the algorithm
	#if affiliation is only one word, then only use affiliation field to do the match
	#return an updated fieldList and boost dictionary
	
		if "processed_aff" in fieldList:
			if(len(student["affiliation"].strip()) == 0):
				fieldList.remove("processed_aff")
				del(boosts['processed_aff'])
			#if the student's input can not make a bigram
			elif(isOneWord(student["affiliation"])):
				#remove the processed_aff fields
				fieldList.remove("processed_aff")
				del(boosts['processed_aff'])
				
				#add the affiliation field since there is only one word
				fieldList.append("affiliation")
				boosts['affiliation']=1.0

			print "fieldList is", fieldList
		return fieldList,boosts

	def validateArguments(self,student,fieldList,boosts):
	#student must have an interest field, processed_aff must be a bigram
	#return true if boost has the same fields as fieldList and they are all floats
		assert len(student["interest"].strip()) > 1, "Student must have an interest"		
		assert len(boosts.keys()) == len(fieldList),"fieldList and boost must have the same keys" 
		
		if boosts:
				try:
						for field in fieldList:
								#all values in boost must be a float
								isinstance(boosts[field],float)
						return True

				#boost must have the same keys as fieldList
				#return false if boost[field] does not exist
				except:
						return False
		
		return False

	def getProfMatch(self,student, numResults = 3, fieldList = ["interest","processed_aff"],boosts={'interest':1.45,'processed_aff':1.0}):
	#student_profile is a dictionary with keys:
	#name, interest, affiliation 
	#boost must be a dictionary where the key is the interest and the boost is the value
	#by default "interests" = 1.25
	#           "processed_aff" = 1.0

		if(self.validateArguments(student,fieldList,boosts)):
			self.fieldList,boosts = self.updateArguments(student,fieldList,boosts)

		query = self.getQuery(student,self.fieldList,boosts)
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
