import numpy as np

tOpen = 900
lamda = 10
tClose = 1700
tNL = 0
tCurrent = 0



class AmusementPark:
	def __init__(self, tFastService, tSlowService):
		self.lower = tFastService
		self.higher = tSlowService
		self.tCurrent = 900

	def doService(self):
		return np.random.uniform(self.lower, self.higher)

	# def setTime(self, tService):
	# 	if tCurrent[]

class QuickPass:
	def __init__(self, tSystem):
		self.tRun = tSystem
		self.vq = 0

	def getTime(self):
		return tCurrent + self.tSystem

ap = AmusementPark(23,28)
# for i in range(16):
	# print ap.doService()
# a = np.random.exponential(lamda,200)
# print a