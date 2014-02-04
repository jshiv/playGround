'''funBox is a generic file for holding generic use functions'''
import math
import pandas as pd
import numpy as np
import re

def list2Str(list, sep = None, cap = None, capIn = None ):
	'''Takes a list and returns a comma separated string
	list = [10,20,30]
	--> listStr = (10,20,30)
	if list = ['AA','AB','BB']
	--> listStr = ("AA","AB","BB")'''
	
	#set defalut Values
	if sep is None:
		sep = ', ' #the default seperator is a space
	if cap is None:
		cap = '()' #the defalut end strings are perenthesies
	
	capInTest = ''
	if capIn is None:
		capInTest = None
		capIn = '"' #default value is to incapsulate each value with Perenthesies
		
	
	s = ""
	for val in list:
		if isStr(val) or capInTest is not None:
			tmpStr = ' '+ capIn + str(val) + capIn
		else:
			tmpStr = ' ' + str(val) #create a temp veriable with a space included
		s += tmpStr 
	s = s.lstrip() #remove left white space
	s = s.replace(' ',sep) #replace white space with the chosen seperator
	s = cap[0]+ s + cap[1] #surround with parenthesis 
	return s
	
	
from types import *	
def isStr(val):
	'''isStr tests a value for being a string 
	and returns true or false'''
	if type(val) is StringType:
		return True
	else:
		return False
		
		
def tupleSet2list(tupleSet, itemIdx = None):
	'''loops over the a set of tuples and builds a vector list from the items in itemIndex'''
	if itemIdx is None:
		itemIdx = 0 #default returns a vector made of the 0th column of the tuple set
	itemList = []
	for item in tupleSet:
		itemList.append(item[itemIdx])
	return itemList
	
	
def timestamp2Date(df, dataCat):
	'''loops over a pandas dataframe and searces for unix timestamps
		returns a dataframe with all timestamps converted to datetimes'''
	
	header = df.columns.values.tolist()
	col2Chg = []
	for col in header:
		val = df[col][0]
		try:
			cat = dataCat[col]
			if cat is 'date':

				col2Chg.append(col)	
		except:
			print "column %s is not catagorized" % col
		#try:#Only allows numbers past
		#	cat = dataCat[col]
		#	digits = intDigits(val)
		#	#if digits is 10 and cat is 'date':# Selects dates grater then '09-Sep-2001 01:46:40' and tries to exclude columns with id labels
		#	if cat is 'date':
		#		col2Chg.append(col)
		#except:
		#	pass
	print col2Chg
	for col in col2Chg:
		df[col] = pd.to_datetime(df[col], unit = 's')
		#df[col] = pd.Series(df[col],dtype = 'datetime64[ns]')
	return df
			
	#now convert the columns in col2Chg into datetime

def headerCat(header, catDict):
	'''loops over the headers of pandas dataframe and looks for matches in the headers
	and tests values for patterns
	lookIn dict is like {'catigory': 'words','to','search','for'}'''

	dataCat = {}
	for col in header:
		for key, subStrList in catDict.items():
			if strTest(subStrList, col.lower()):
				dataCat.update({col:key})
	return dataCat			
		
		
def headerType(df):
	'''loops over the headers of pandas dataframe and tests non-null values for a their type
		returns a dict of {header: datatype}'''
	dataTypes = {
	'INTEGER': ['int'],
	'DOUBLE': ['float'],
	'BOOLEAN': ['bool'],
	#'DATE': ['date'],
	'DATETIME': ['datetime'],
	'CHAR_STRING': ['str']}
	header = df.columns.values.tolist()
	
	dataType = {}
	typTmp = []
	for col in header:
		dfTmp = df[col][df[col].notnull()]

		dt = dfTmp.dtype
		for key, typeList in dataTypes.items():
			#test if the data types string matches any in the given types list
			try:
				if strTest(typeList, dt.name):
					typTmp = key
				elif dt.name in 'object':
					val = dfTmp[0]
					typTmp = typeTest(val)
				else:
					typTmp = []

				if typTmp != []:
					dataType.update({col:typTmp})
			except:
				pass
				#dataType.update({col: 'NULL'})
	return dataType
	
	
def typeTest(val):
	try:
		intdigits = intDigits(val)
		allDigits = len(str(val))
		if allDigits is intdigits:
			dType = 'INTEGER'
		else:
			dType = 'FLOAT'
	except:
		dType = 'CHAR_STRING'
		
	return dType
		
		
		
		
'''		
#algorythim structure from
#http://ryrobes.com/python/build-tableau-data-extracts-out-of-csv-files-more-python-tde-api-madness/
def datatyper(n):    # force some data types to figure shit out
	try:         # kind of lame.... BUT IT WORKS
		x = int(n)
		return int(n)
	except:
		try:
			x = float(n)
			return float(n)
		except:
			try:
				date_object = datetime.strptime(n, '%m/%d/%Y')
				return date_object
			except:
				try:
					date_object = datetime.strptime(n, '%Y-%m-%d')
					return date_object
				except:
					if n == 'NULL': # just in case, don't want any literal NULLs in there
						return None
					elif len(n) > 0:
						return str(n)
					else: # no need to return an empty string, let's NULL that shit out
					return None'''
									
									
def strTest(strA, strB = None):
	'''
	if strA is a single value, and strB is a single value
		strA == strB?
	if strA is a list and strB is a single value
		any(strA[1,2,3,...]) in strB? --> True/False
	if strA is a single value and strB is a list
		strA == strB(i) --> boolean vector len(strB)
	if strA is a list and strB is a list
		strA(i) == any(strB) --> boolean vector len(strA)'''
	
	if strB is None:
		#test if strA is a string or not
		tf = isinstance(strA,basestring)
	elif isinstance(strA,basestring) and isinstance(strB,basestring):
		'''strA is string
		strB is string'''
		tf = (strA == strB)
	elif isinstance(strA,basestring) and not isinstance(strB,basestring):
		'''strA is string
		strB is list'''
		#test for substring A existing in any of the strings in list B
		tf = any(strA in s for s in strB)
	elif not isinstance(strA,basestring) and isinstance(strB,basestring):
		'''strA is list
		strB is string'''
		#test for any of the substring A items existing in string B
		tf = any(s in strB for s in strA)
	elif not isinstance(strA,basestring) and not isinstance(strB,basestring):	
		'''strA is a list
		strB is a list'''
		# test if any of the substrings in A match any of the strings in B
		tf = any(a in b for a in strA for b in strB)
	return tf
	
	

def intDigits(n):
	if n > 0:
		digits = int(math.log10(n)) + 1
	elif n == 0:
		digits = 1
	else:
		digits = int(math.log10(-n)) + 1
	return digits


def obj2List(obj):
	'''Converts any single object that is nto a list(string, class, object, number ect...)
	to the 0th instance of a list'''
	objList = []
	if isinstance(obj, list):
		objList = obj
	else:
		objList.append(obj)

	return objList
	
#http://stackoverflow.com/questions/5849800/tic-toc-functions-analog-in-python
class Timer(object):
	def __init__(self, name=None):
		self.name = name

	def __enter__(self):
	    self.tstart = time.time()

	def __exit__(self, type, value, traceback):
		if self.name:
 			print '[%s]' % self.name,
		print 'Elapsed: %s' % (time.time() - self.tstart)
	
	
	
	
	
if __name__ == "__main__":
	vecTypeTest(df)
	'''
	strA = ['id','Id','ID']
	strB = ['date','Date','DATE','time','Time','TIME']
	tf = strTest(strA,strB)'''
