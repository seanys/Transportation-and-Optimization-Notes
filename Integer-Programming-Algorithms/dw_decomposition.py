'''
类型：Dantzig Wolfe Decomposition
原理：该算法主要应对部分约束较为复杂的情况，将其进行分解，与Bender的差异是，
Bender是部分变量较为复杂，求解过程中，Bender是通过求解子问题，给主问题增加
约束，而DW解出子问题后，会增加基变量，这一点类似于Column Generation。

源码：还在写！！！！！！原理和DW
'''
from pulp import * # 基于Pulp
import random  # 生成随机数

class MasterProblem:
	'''主问题
	
	'''
	def __init__(self, maxValue, itemLengths, itemDemands, initialPatterns, problemname):
		
		self.maxValue=maxValue
		self.itemLengths=itemLengths
		self.itemDemands=itemDemands
		self.initialPatterns=initialPatterns
		
		self.prob = LpProblem(problemname,LpMinimize)	# 建立初始问题
		
		self.obj = LpConstraintVar("obj")   # 建立目标函数的约束变量
		self.prob.setObjective(self.obj)
		
		self.PatternVars = []
		self.constraintList = []   # 约束函数部分
		for i,x in enumerate(itemDemands):		# 建立主问题的全部约束
			var = LpConstraintVar("C"+str(i),LpConstraintGE,x) 
			self.constraintList.append(var)
			self.prob += var
			
		for i,x in enumerate(self.initialPatterns):  # 建立初始的解
			temp = []
			for j,y in enumerate(x):
				if y > 0: 
					temp.append(j)
			
			var = LpVariable("Pat"+str(i)	, 0, None, LpContinuous, lpSum(self.obj+[self.constraintList[v] for v in temp]))  # create decision variable: will determine how often pattern x should be produced
			self.PatternVars.append(var)
		
	def solve(self): 
		self.prob.writeLP('res/prob.lp')
		self.prob.solve()
		
		return [self.prob.constraints[i].pi for i in self.prob.constraints]


	def addPattern(self,pattern):
		'''增加新的Pattern'''		
		self.initialPatterns.append(pattern)
		temp = []
		
		for j,y in enumerate(pattern):
			if y>0: 
				temp.append(j)
		
		var = LpVariable("Pat"+str(len(self.initialPatterns))	, 0, None, LpContinuous, lpSum(self.obj+[pattern[v]*self.constraintList[v] for v in temp]))
		self.PatternVars.append(var)
		
	
	def startSub(self,duals):
		'''解SubProblem求解新的Pattern'''
		newSubProb = SubProblem(duals,self.itemLengths,self.maxValue)
				
		pattern = newSubProb.returnPattern()
		return pattern
		
	def setRelaxed(self,relaxed):
		'''如果没有找到新的Patterns，那么按照整数规划求解'''
		if relaxed == False:
			for var in self.prob.variables():
				var.cat = LpInteger
			
	def getObjective(self):
		return value(self.prob.objective)
		
	def getUsedPatterns(self):
		usedPatternList=[]
		for i,x in enumerate(self.PatternVars):
			if value(x)>0:
				usedPatternList.append((value(x),self.initialPatterns[i]))
		return usedPatternList
		

class SubProblem(object):
	'''子问题建立
	思路：通过对偶问题求目标参数，以及约束，解出后如果目标函数符合
	条件，则在Pattern中增加新的变量，然后进入下一轮求解
	'''
    def __init__(self,duals, itemLengths,maxValue):
        self.subprob = LpProblem("Sub problem solver",LpMinimize)
        self.varList = [LpVariable('S'+str(i),0,None,LpInteger) for i,x in enumerate(duals)]
        self.subprob += -lpSum([duals[i]*x for i,x in enumerate(self.varList)])  # 建立对偶问题
        self.subprob += lpSum([itemLengths[i]*x for i,x in enumerate(self.varList)]) <= maxValue 

        self.subprob.writeLP('res/subprob.lp')
        self.subprob.solve() 
        self.subprob.roundSolution()

    def returnPattern(self):
		'''判断是否可以解'''
        pattern = False
        if value(self.subprob.objective) < -1.00001:
            pattern = []
            for v in self.varList:
                pattern.append(value(v))
        return pattern
	
		
random.seed(2012)

nrItems = 12
lengthSheets=20


itemLengths=[]
itemDemands=[]

# 生成整个的约束变量
while len(itemLengths) != nrItems:
	length = random.randint(5, lengthSheets-2)
	demand = random.randint(5, 100)
	if length not in itemLengths:
		itemLengths.append(length)
		itemDemands.append(demand)
	
print("Item lengts  : %s" % itemLengths)
print("Item demands : %s\n\n" % itemDemands)

# 随机生成问题
patterns = []
print("Generating start patterns:")
for x in range(nrItems):
	temp = [0.0 for y in range(x)]
	temp.append(1.0)
	temp += [0.0 for y in range(nrItems-x-1)]
	patterns.append(temp)
	print(temp)

# 解Master Problem
print("\n\nTrying to solve problem")
CGprob = MasterProblem(lengthSheets,itemLengths,itemDemands,patterns,'1D cutting stock')
	
# 进行持续性松弛，解SubProblem，直到没有更优解
relaxed = True
while relaxed == True:
	duals = CGprob.solve()
	
	newPattern = CGprob.startSub(duals)
	
	print('New pattern: %s' % newPattern)
	
	if newPattern:
		CGprob.addPattern(newPattern) # 找到新的Pattern就开始求解
	else:
		CGprob.setRelaxed(False) # 没有找到新的Pattern，就按照整数规划方式求解
		CGprob.solve()
		relaxed=False

print("\n\nSolution: %s sheets required" % CGprob.getObjective())

t=CGprob.getUsedPatterns()
for i,x in enumerate(t):
	print("Pattern %s: selected %s times	%s" % (i,x[0],x[1]))
