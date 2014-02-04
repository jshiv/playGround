'''statBox: Provides a set of Objects for the pupurose of generating random numbers 
	that fit various continuous probability distributions
Title: statBox
Created in 8Jan2014

@author: Jason Shiverick
@corp: Tesla Motors
'''

from scipy import stats

import random
import matplotlib.pyplot as plt
import warnings
import pandas as pd
import numpy as np
import datetime as dt
import funBox as fb
import pdb
# just for surpressing warnings
warnings.simplefilter('ignore')

''' TO DO:
1)  Add timestamps in the plot
2)  Add suspension data

'''
class dist:
	'''Contains properties specific to the generated continuous probability distribution
		parmList is a set of parameters that acompanie the given distName
		example usage:
		import statBox as sb
		reload(sb)
		exObjA = sb.dist(distName = 'weibull_min', param = (1,2, 1))
		Data = exObjA.rv.rvs(150)
		exObjB = sb.dist(X = Data)
		exObjC = sb.dist(rvObj = exObjB.rv)
		'''

	distNamesList = ["cauchy", "chi2", "norm", "expon", "exponweib", "f", "gamma", "genextreme", "invgamma", "lognorm", "logistic", "t", "uniform",   "alpha", "beta", "weibull_min", "burr", "weibull_max"]
	base = dt.datetime.today().date()
	def __init__(self, X = None, distName = None, param = None, rvObj = None):
			

		if rvObj is None:
			if distName is not None:
				#pdb.set_trace()
				self.rv, self.theta = distFit(distName, X, param)
			else:
				self.rv, self.theta, self.fit_df = distWiz(X, self.distNamesList)
		else:
			self.rv = rvObj

		if X is None:
			self.X = self.rv.rvs(50)

		else:
			self.X = X

		self.distName = self.rv.dist.name


	def montyCarlo(self , sampleSize = None):
		'''This is an example of how the rv object can be used'''
		return self.rv.rvs(	size = sampleSize)



	def plot(self):
		'''Generates a probability plot and pdf plot of the given distribution and data'''

		x = np.linspace(np.maximum(self.rv.dist.a, min(self.X)), np.minimum(self.rv.dist.b, max(self.X)))

		# Formatting the graoh area
		fig = plt.figure(figsize=(16, 9))

		#Probability plot in upper right hand corner
		ax1 = plt.subplot(221)
		stats.probplot(x = self.X, sparams = self.rv.args,dist=self.rv.dist.name, fit=False, plot=plt)
		plt.title(self.rv.dist.name + ' Pr')


		#CDF in upper right hand corner
		ax2 = plt.subplot(222)
		ax2.plot(x, self.rv.cdf(x))
		plt.title(self.rv.dist.name + ' CDF')

		ax2.hist(self.X, normed=1,alpha=.3, cumulative=True)


		#PDF in lower right left corner
		ax4 = plt.subplot(224)
		ax4.plot(x, self.rv.pdf(x))
		plt.title(self.rv.dist.name + ' PDF')

		ax4.hist(self.X, normed=1,alpha=.3)		


		#Scatter plot in lower left hand corner
		ax3 = plt.subplot(223)
		#df = pd.DataFrame(np.random.randn(10,2), columns=['col1','col2'])
		#base = dt.datetime.today()
		#dateList = [ base - dt.timedelta(days=x) for x in range(0,10) ]
		#df["timestamp_utc"] = dateList
		ax3.scatter(range(len(self.X)), self.X, alpha=.3)
		plt.title("Scatter Plot")

		plt.show()


def rndPerm(dataObj, n, seedVal= None):
    ''' Select randomly n elements for a data Object transforming it 
    in a dataframe and selecting random indexes. It returns a dataframe'''
    if seedVal is not None:
			random.seed(seedVal)
    df = dataObj.df
    df = df.ix[random.sample(df.index,n)]    
    return df


def distFit(distName, X = None, params = None):
	'''Creates a frozen probabilitiy object in the form of scipy.stats.distName
	distName: required variable
	X: distName will fit to data in X
	theta: either a full or partial list of parameters to set a distribution object'''
	# fit our data set against every probability distribution
	if params is None and X is not None:
		theta = eval("stats."+distName+".fit(X)")
	elif params is not None and X is None:
		theta = params
	elif params is not None and X is not None:
		frstMoment = params[0]
		scntMoment = params[1]
		theta = eval("stats."+distName+".fit_loc_scale(X, [frstMoment, scndMoment])")
	

	if len(theta) == 4:
		distObj = eval("stats." + distName + ".freeze(theta[0],theta[1],loc = theta[2], scale = theta[3])")
	elif len(theta) == 3:
		distObj = eval("stats." + distName + ".freeze(theta[0], loc = theta[1], scale = theta[2])")
	elif len(theta) == 2:
		distObj = eval("stats." + distName + ".freeze(loc = theta[0], scale = theta[1])")
	else:
		distObj = eval("stats." + distName + ".freeze(loc = theta[0])")
	return distObj, theta


def distWiz(X, distNames):
	'''Loops over the list of distribution Names and fits the data in X to each'''
	distSet = pd.DataFrame( columns = ['sampleSize', 'nbrParameters', 'theta', 'distObj' ,'nLogL', 'ksStat', 'AICc'], index = distNames)
	testSet = pd.DataFrame( columns = ['nLogL', 'kstest', 'AICc'], index = distNames)
	#print distSet
	#print fitSet
	for distName in distNames:
		#print distName
		# fit our data set against every probability distribution
   		
		distObj, theta = distFit(distName, X = X)
   		#Applying the negative log likelihood test
   		
   		nLogL = eval("stats."+distName+".nnlf( theta, X)")
   		
   		#Applying the Kolmogorov-Smirnof one sided test
		D, p = stats.kstest(X, distName, args=theta)
		
		k = len(theta) #number of parameters
		n = len(X) #Sample Size
		#BIC = -2*(nnlfTest) + k*math.log(n)
		AIC = 2*k - 2*(-nLogL)
		
		AICc = AIC + 2*k*(k+1)/(n-k-1)


		distSet['nLogL'][distName] = nLogL
		distSet['ksStat'][distName] = D
		distSet['nbrParameters'][distName] = k
		distSet['sampleSize'][distName] = n
		distSet['AICc'][distName] = AICc
		distSet['theta'][distName] = theta
		distSet['distObj'][distName] = distObj

	bestFitDist, topFive = statRank(distSet[['nLogL','ksStat','AICc']], rankWeight = [.33, .33, .33])
	return  distSet.loc[bestFitDist[0],'distObj'], distSet.loc[bestFitDist[0],'theta'], distSet.loc[topFive, :]

def statRank(rankSet, rankWeight = None):
	'''find the mean weighted rank of each test statistic
	rankSet is a DataFrame where columns = test statistics and the Index are Distribution Names
	rankWeight is a list of weighting for each corisponding test statistic '''


	if rankWeight is None:
		#create a rankWeight list that is equal weighting
		rankWeight = []
		for i in range(rankSet.shape[1]):
			rankWeight.append((1/float(rankSet.shape[1])))

	#convert the rankSet df to a rankIndex df
	#header = rankSet.columns.values.tolist()
	distList = rankSet.index.tolist()
	dfRank = rankSet.rank(numeric_only=None, method='min', na_option='bottom', ascending=True)

	meanRankSet = pd.Series( index = distList)
	for distName in distList:
		dfTmp = dfRank.loc[distName,:]*rankWeight
		mwr = np.mean(dfTmp.tolist())
		meanRankSet[distName] = mwr
	finalRank = meanRankSet.rank()

	topFive = finalRank[finalRank <= 5]
	topFive = topFive.order()
	bestFitDist = finalRank[finalRank == 1]

	return bestFitDist.index.tolist(), topFive.index.tolist()



if __name__ == "__main__":
	#random.seed(87655678)
	X = stats.weibull_min(1,2, 1).rvs(100)
	obj = dist(X = X)