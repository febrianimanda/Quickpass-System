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

class AmusementPark:
	def __init__(self):
		self.lower = 23
		self.higher = 28
		self.runtime = {}
		self.initAllPlayingTime()
		self.shiftkuota = {}
		self.initKuota()

	def doService(self):
		return np.random.uniform(self.lower, self.higher)

	def chanceQuickPass(self):
		return np.random.uniform(0,1)

	def showShiftKuota(self):
		for i in range(0,len(self.shiftkuota)):
			print i, '|', self.shiftkuota[i]

	def initKuota(self):
		for i in range(0, len(self.runtime)):
			self.shiftkuota[i] = 20

	def getShiftKuota(self, index):
		return self.shiftkuota[index]

	def initAllPlayingTime(self):
		for i in data:
			self.runtime[i] = data[i]['play']

	def getRuntime(self):
		return self.runtime

	def checkAvailableTime(self, index):
		return True if tCurrent+self.mintime < self.rangetime[index]['start'] else False

	def checkAvailableKuota(self, index):
		return True if self.getShiftKuota(index) > 0 else False

	def addQueue(self, index):
		if self.checkAvailable(index) and self.checkAvailableKuota(index):
			if self.kuota[index] < 1 :
				self.kuota[index] = self.kuota[index] - 1
			else :
				print "Maaf yang anda pilih sudah tidak tersedia"	
		else :
			print "Maaf yang anda pilih sudah tidak tersedia"

class QuickPass:
	def __init__(self, tSystem):
		self.tRun = tSystem
		self.vq = 0
		self.rangetime = {}
		self.availabletime = []
		self.mintime = 20
		self.treshold = 0.3

	def checkAvailable(self, index):
		return True if tCurrent+self.mintime < self.rangetime[index]['start'] else False

	def setupAvailableShift(self):
		if self.rangetime != []:
			for i in self.rangetime:
				if self.checkAvailable(i):
					self.availabletime.append(i)
		else :
			print "Maaf range waktu belum ada"
		
	def setupRangeTime(self):
		for i in range(1,len(data)):
			self.rangetime[i] = {
				'start' : data[i]['start'],
				'finish' : data[i]['end'],
			}

	def start(self):
		self.setupRangeTime()
		self.setupAvailableShift()

	def showAvailableShift(self):
		if self.availabletime != []: 
			ap = AmusementPark()
			for i in self.availabletime:
				print i, '|', self.rangetime[i]['start'], '-', self.rangetime[i]['finish'], '|', ap.getKuota(i)
		else :
			print "Maaf waktu tersedia belum ada"

	def getKuota(self):
		return self.kuota

	def doQuickpass():
		self.showAvailableShift()

qp = QuickPass(0)
tCurrent = 910
ap = AmusementPark()
qp.start()
# print qp.rangetime[3]
# print qp.availabletime
# qp.showAvailableShift()

# simulation = {}
# for i in range(10):
# 	simulation[i] = np.random.exponential(lamda,100)

print "Pengunjung ke- \t Waktu Kedatangan(Jam) \t Rentang Waktu kedatangan (Menit) \t Pilihan Antrian \t Interval Waktu Kembali \t Mulai Layanan \t Lama Waktu Antri \t Nomor Antrian"

# print simulation