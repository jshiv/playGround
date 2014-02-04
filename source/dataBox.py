# -*- coding: utf-8 -*-
'''
Title: dataBox
Created on Thurs Jan 2nd 2014 12:05 PM

@author: JShiverick
@corp: Tesla Motors

	dataBox contains classes methods and properties that pertain to the 
	orginization and processing of various data strucutes
	
	Purpose:
		A: Organize data returned from sqlQuerys into pandas.DataFrame
			- Identify and convert columns in the data frame from str to the appropriate data type
		B: Manipulate Object Properties between json structure and dataFrame
		C: Identify and catalog categories of data for future analysis
			-i.e.(sig_value:{Temperature || Voltage || ect...} dateValue:{latest update || signal date || ect...}
		
		
'''
import pdb
import numpy as np
import pandas as pd
import funBox as fb
import random

class data:
	'''data contains the properties that orginaze the given data into varios types and structures:
		rawData: the data given to the data class
		df: data transformed into a pandas.dataframe
		json: data transformed to json format
		catObj: contains properties that attempt to type and catagorize each column of data'''
		
	rawData = []
	rawType = []
	npArray = []
	df = []
	json = []
	catObj = []
	dictSet = []
	listSet = []
	dataCat = []
	dataType = []
	
	descObj = []
	header = []
		
	def __init__(self, rawData, lean = False):
		'''takes in data from rawData
			lean is True: only renders df to save space and time'''
		self.rawData = rawData

			
	def testType(self):
		'''testType saves the data type and a pandas.Series of the type of each column'''
		self.rawType = type(rawData)


	def setHeader(self, header = None , mysqlDesc = None):
		'''allows for direct input of a header list or a mysql cursor description tuple set
			if both are given, accept the user input header and create a mysqlType Object'''
		
		if mysqlDesc is not None:
			self.descObj = cursorDesc(mysqlDesc)
			self.header = self.descObj.headerList
		
		if header is not None:
			self.header = header

		
	def testCat(self):
		pass

	def cat(self):
		pass

	def jsonMake(self):
		if not self.df:
			self.dfMake()
			
		self.json = pd.DataFrame.to_json(self.df)

	def dfMake(self):
		# Here we have a problem with empty
		'''converts a given np array to a pandas.DataFrame'''
		if not self.npArray:
			self.arrayMake()
		if not self.header:
			df = pd.DataFrame(self.npArray)
		else:
			# This is giving me problem
			df = pd.DataFrame(self.npArray, columns = self.header)
			
		df = df.convert_objects(convert_numeric = True, convert_dates = True)
		
		self.findCat(df)
		self.df = timestamp2Date(df, self.dataCat)
		self.findType(self.df)
		
	def arrayMake(self):
		'''converts a given list into a numpy.array'''
		self.npArray = np.array(self.rawData)
		
	def findCat(self, df = None):
		'''vecType tests the headers and values in the 
		columns of a dataframe to guess at the type of data contained in each'''
		if df is None:
			df = self.df
		#vecDict is a dictionary of {header : datatype}	
		catDict = {
		'id': ['id','vin'],
		'date': ['date','time','birthday'],
		'data': ['sig','value','cycle','count','odometer']}
		header = df.columns.values.tolist()
		self.dataCat = headerCat(header, catDict) 
		
	def findType(self, df = None):
		'''findType scans the data and returns a dictionary that describes the type of data in each column
		if ccursorDesc has been run, it evaluates aginst the predefined dictionary from a query'''
		if df is None:
			df = self.df

		self.dataType = headerType(df)
		


			

	
class cursorDesc:
	'''Takes in a MySQL cursor.description and saves
		description: the given description
		typeSet: a dataframe with header labes for rows and columns (mysqlType Label, pythonType)
		mysql description is structured as
		(column_name,
				type,
				None,
				None,
				None,
				None,
				null_ok,
				column_flags)'''
	desc = []
	headerList = []
	typeList = []
	typeSet = []
	field_type = {
	0: 'DECIMAL',
	1: 'TINY',
	2: 'SHORT',
	3: 'LONG',
	4: 'FLOAT',
	5: 'DOUBLE',
	6: 'NULL',
	7: 'TIMESTAMP',
	8: 'LONGLONG',
	9: 'INT24',
	10: 'DATE',
	11: 'TIME',
	12: 'DATETIME',
	13: 'YEAR',
	14: 'NEWDATE',
	15: 'VARCHAR',
	16: 'BIT',
	246: 'NEWDECIMAL',
	247: 'INTERVAL',
	248: 'SET',
	249: 'TINY_BLOB',
	250: 'MEDIUM_BLOB',
	251: 'LONG_BLOB',
	252: 'BLOB',
	253: 'VAR_STRING',
	254: 'STRING',
	255: 'GEOMETRY' }
	
	def __init__(self, desc):
		'''desc comes from cursor.description'''
		self.desc = desc
		self.getType()
		
	def getHeader(self):
		'''Return a list of the headders in the 0th column of the description'''
		self.headerList = fb.tupleSet2list(self.desc, itemIdx = 0)
	
	def getType(self):
		if not self.headerList:
			self.getHeader()
		intTypeList = fb.tupleSet2list(self.desc, itemIdx = 1)
		for intType in intTypeList:
			mysqlType = self.field_type[intType]
			mysqlType = mysqlType.lower()
			self.typeList.append(mysqlType)
		
		self.typeSet = dict(zip(self.headerList,self.typeList))


### Cleaning Functions
def timestamp2Date(df, dataCat):
	'''loops over a pandas dataframe and searces for unix timestamps
		returns a dataframe with all timestamps converted to datetimes'''
	
	header = df.columns.values.tolist()
	col2Chg = []
	for col in header:
		val = df[col][0]
		dtypeName = df[col].dtype.name
		try:
			cat = dataCat[col]
			if cat is 'date' and fb.strTest(['date','time'],dtypeName) is False:

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


def headerCat(header, catDict):
	'''loops over the headers of pandas dataframe and looks for matches in the headers
	and tests values for patterns
	lookIn dict is like {'catigory': 'words','to','search','for'}'''

	dataCat = {}
	for col in header:
		for key, subStrList in catDict.items():
			if fb.strTest(subStrList, col.lower()):
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
				if fb.strTest(typeList, dt.name):
					typTmp = key
				elif dt.name in 'object':
					val = dfTmp[0]
					typTmp = fb.typeTest(val)
				else:
					typTmp = []

				if typTmp != []:
					dataType.update({col:typTmp})
			except:
				pass
				#dataType.update({col: 'NULL'})
	return dataType

if __name__ == "__main__":
	from connBox import mysqlConn
	connObj = mysqlConn(dbName = 'claw')
	#pdb.set_trace()
	sql = 'select id, vin, birthday, from_unixtime(delivery_date) as delivery_date from claw.vehicles where vin like ("5yjs%") limit 10'
	df = connObj.runQuery(sql)
	connObj.drop()











































		