import csv
import numpy as np

data = {}

with open('running.csv', 'rb') as csvfile:
  reader = csv.DictReader(csvfile,delimiter=',')
  for row in reader:
  	data[int(row['run'])] = {
  		'start' : int(row['start']),
  		'end'		: int(row['end']),
  		'play'	: int(row['play'])
  	}

tOpen = 900
lamda = 10
tClose = 1700
tNL = 0
tCurrent = 0

def getAllPlayingTime():
	plays = {}
	for i in data:
		plays[i] = data[i]['play']
	return plays

def getRangeTime():
	period = {}
	for i in range(1,len(data)):
		period[i] = {
			'start' : data[i]['start'],
			'finish' : data[i]['end'],
		}
	return period

class AmusementPark:
	def __init__(self, tFastService, tSlowService):
		self.lower = tFastService
		self.higher = tSlowService
		self.runtime = getAllPlayingTime()

	def doService(self):
		return np.random.uniform(self.lower, self.higher);

class QuickPass:
	def __init__(self, tSystem):
		self.tRun = tSystem
		self.vq = 0
		self.rangetime = getRangeTime()
		self.kuota = {}
		for i in range(len(self.rangetime)):
			self.kuota[i+1] = 20

	def getTime(self):
		return tCurrent + self.tSystem

	def showAvailableTime(self):
		for i in self.rangetime:
			if tCurrent < self.rangetime[i]['start']:
				print i, '|', self.rangetime[i]['start'], '-', self.rangetime[i]['finish']

	def addQueue(self, index):
		self.kuota[index] = self.kuota[index] - 1


qp = QuickPass(0)
qp.showAvailableTime()
qp.addQueue(4)
# ap = AmusementPark(23,28)
# print ap.doService()
# # for i in range(16):
# 	# print ap.doService()
# # a = np.random.exponential(lamda,200)
# # print a