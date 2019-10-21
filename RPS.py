import random
import pickle
import numpy as np
import eel
import os
class faded_AI():
	def __init__(self,dim):
		self.is_AI=1
		self.dim=dim
		self.learning=1
		self.dic={}
		self.pairs_keep=[]
		self.learning_rate=1
		self.constant_mistakes=0
		self.last_x=[]
		for i in range(self.dim):
			self.pairs_keep.append([])
		self.count=0
		self.w=[]
		for i in range(3):
			self.w.append(np.zeros(dim+1))
	def clear(self):
		self.dic={}
		self.pairs_keep=[]
		self.learning_rate=1
		self.constant_mistakes=0
		for i in range(self.dim):
			self.pairs_keep.append([])
		self.count=0
		self.w=[]
		for i in range(3):
			self.w.append(np.zeros(self.dim+1))		
	def load(self,filename):
		f=open(filename,'rb')
		(self.count,self.dim,self.learning_rate,self.constant_mistakes,self.w,self.last_x,self.pairs_keep,self.dic)=pickle.load(f)  
	def save(self,filename):
		f=open(filename,'wb')
		pickle.dump((self.count,self.dim,self.learning_rate,self.constant_mistakes,self.w,self.last_x,self.pairs_keep,self.dic),f)
	def feed(self,pair):
		self.count+=1
		for i in range(self.dim):
			if len(self.pairs_keep[i])==i+1:
				if tuple(self.pairs_keep[i]) not in self.dic:
					self.dic[tuple(self.pairs_keep[i])]=[0,0,0]
				self.dic[tuple(self.pairs_keep[i])][pair[1]-1]+=1
				del self.pairs_keep[i][0]
			self.pairs_keep[i].append(pair)
		if self.learning==1:
			learning_change=1.2
			if pair[1]==pair[0]%3+1:
				self.w[(pair[1]-1)%3]+=self.learning_rate*1*self.last_x[(pair[1]-1)%3]
				self.w[(pair[0]+1)%3]-=self.learning_rate*1*self.last_x[(pair[0]+1)%3]
				self.constant_mistakes+=1
				if self.learning_rate*pow(learning_change,self.constant_mistakes)>1:
					self.learning_rate=1					
				else:
					self.learning_rate*=pow(learning_change,self.constant_mistakes+1)
				self.learning_rate=1
			elif pair[1]==pair[0]:
				self.w[(pair[1]-1)%3]+=self.learning_rate*0.5*self.last_x[(pair[1]-1)%3]
				self.w[(pair[0]+1)%3]-=self.learning_rate*0.5*self.last_x[(pair[0]+1)%3]
			else:
				self.constant_mistakes=0
				self.learning_rate/=learning_change
	def get_result(self):
		x=[]
		for i in range(3):
			x.append(np.zeros(self.dim+1))
			#######
			x[i][self.dim]=1
		for i in range(len(self.pairs_keep)):
			if self.count-i<=0:
				break
			tup=tuple(self.pairs_keep[i])
			#print(self.dic)
			if tup not in self.dic:
				for j in range(3):
					x[j][i]=0
			else:
				sumi=0
				for j in range(3):
					sumi+=self.dic[tup][j]
				for j in range(3):
					x[j][i]=self.dic[tup][j]/sumi
		self.last_x=x
		result_lis=[]
		for i in range(3):
			result_lis.append(np.dot(self.w[i],x[i]))
		return (random.choice(list(np.where(result_lis==np.max(result_lis))[0]))+1)%3+1
AI=faded_AI(4)
AI.clear()
result_list=[]
@eel.expose
def remove():
	del result_list[0]
@eel.expose
def deal(i):
	result=AI.get_result()
	result_list.append(result)
	with open('data.txt', 'w') as f:
		for each in result_list:
			f.write(str(each)+'\n')	
	AI.feed((result,i))
	if i==result:
		print('tie')
	elif (i+1)%3+1==result:
		print('win')
	else:
		print('los')	
eel.init(os.getcwd())
eel.start('RPS.html')
