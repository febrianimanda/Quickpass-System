import csv
import numpy as np
import random

data = {}

with open('running.csv', 'rb') as csvfile:
  reader = csv.DictReader(csvfile,delimiter=',')
  for row in reader:
  	data[int(row['run'])] = {
  		'start' : int(row['start']),
  		'end'		: int(row['end']),
  		'play'	: int(row['play'])
  	}

class Time:
	def __init__(self):
		self.tHour = 0
		self.tMinutes = 0
		self.tSeconds = 0

	def setHour(self, time):
		self.tHour = time

	def setMinutes(self, time):
		self.tMinutes = time

	def setSeconds(self, time):
		self.tSeconds = time

	def getHour(self):
		return self.tHour

	def getMinutes(self):
		return self.tMinutes

	def getSeconds(self):
		return self.tSeconds

	def getTime(self):
		return self.tHour * 100 + self.tMinutes

	def deconvertingTime(self, time, init=False):
		temp = map(int, str(time))
		if len(temp) == 3:
			if init:
				self.initTime(temp[0], temp[1] + temp[2])
			else:
				return temp[0], temp[1] + temp[2]
		elif len(temp) == 4:
			if init:
				self.initTime(temp[0]*10 + temp[1], temp[2]*10 + temp[3])
			else:
				return temp[0]*10 + temp[1], temp[2]*10 + temp[3]
		else:
			print "deconverting gagal"
			return 0

	def initTime(self, hour, minutes):
		self.setHour(hour)
		self.setMinutes(minutes)
		self.setSeconds(0)

	def runtiming(self, time):
		self.tMinutes += time
		if self.tMinutes >= 60:
			self.tHour += 1
			self.tMinutes -= 60

class AmusementPark:
	def __init__(self):
		self.lower = 23
		self.higher = 28
		self.runtime = {}
		self.initAllPlayingTime()
		self.kuota = 20
		self.shiftkuota = {}
		self.initKuota()

	def chanceQuickPass(self):
		return np.random.uniform(0,1)

	def showShiftKuota(self):
		for i in range(0,len(self.shiftkuota)):
			print i, '|', self.shiftkuota[i]

	def initKuota(self):
		for i in range(0, len(self.runtime)):
			self.shiftkuota[i] = self.kuota

	def getShiftKuota(self, index=-1):
		if index > 0:
			return self.shiftkuota[index]
		else:
			return self.shiftkuota

	def initAllPlayingTime(self):
		for i in data:
			self.runtime[i] = data[i]['play']

	def getAllRuntime(self):
		return self.runtime

	def getRuntime(self, index):
		return self.runtime[index]

	def checkAvailableKuota(self, index):
		return True if self.getShiftKuota(index) > 0 else False

	def addQueue(self, index):
		if self.checkAvailableKuota(index):
			self.shiftkuota[index] = self.shiftkuota[index] - 1
		else :
			print "Maaf yang anda pilih sudah tidak tersedia"

	def getKuota(self):
		return self.kuota

	def getIndexByTime(self, time):
		for i in range(len(self.runtime)):
			if time < self.runtime[i]:
				return i

	def calcWaitingTime(self, indexRuntime, time):
		return self.getRuntime(indexRuntime) - time

class QuickPass:
	def __init__(self, park, tCurrent, percentage):
		self.rangetime = {}
		self.availabletime = []
		self.treshold = 0.3
		self.mintime = 20
		self.kuotapercentage = percentage
		self.queue = {}
		self.kuota = park.getKuota() * percentage / 100
		self.initRangeTime()
		self.initAvailableShift(park, tCurrent)
		self.initQueue()

	def initQueue(self):
		for i in range(1, len(self.rangetime)+1):
			self.queue[i] = 0

	def initAvailableShift(self, park, tCurrent):
		for i in self.rangetime:
			if self.checkAvailableTime(i, tCurrent) and park.checkAvailableKuota(i):
				self.availabletime.append(i)
		
	def initRangeTime(self):
		for i in range(1,len(data)):
			self.rangetime[i] = {
				'start' : data[i]['start'],
				'finish' : data[i]['end'],
			}

	def checkAvailableTime(self, index, tCurrent):
		return True if tCurrent + self.mintime < self.rangetime[index]['start'] else False

	def getIndexAvailableTime(self, tCurrent):
		index = []
		for i in range(1, len(self.rangetime) + 1):
			if tCurrent + self.mintime < self.rangetime[i]['start']:
				if self.checkShiftAvailable(i): 
					index.append(i)
		return index

	def checkShiftAvailable(self, index):
		return self.queue[index] < self.getKuota()

	def showAvailableShift(self, park):
		for i in self.availabletime:
			if park.checkAvailableKuota(i):
				print i, '|', self.rangetime[i]['start'], '-', self.rangetime[i]['finish'], '|', park.getShiftKuota(i)

	def getShiftKuota(self, index):
		return self.queue[index]

	def getKuotaPercentage(self):
		return self.kuotapercentage

	def setKuotaPercentage(self, value):
		self.kuotapercentage = value

	def addQueue(self, index):
		self.queue[index] += 1

	def getQueue(self):
		return self.queue

	def getKuota(self):
		return self.kuota

	def getAllRangetime(self):
		return self.rangetime

	def getRangetime(self, index):
		return self.rangetime[index]

	def getShiftTime(self, index):
		return self.rangetime[i]

	def getTicket(self, time):
		avatime = self.getIndexAvailableTime(time)
		# print "time:", time
		# print "avatime :", avatime
		if avatime != []:
			randQueue = random.randint(avatime[0], avatime[-1])
			# print "rand get ticket:", randQueue
			self.addQueue(randQueue)
			return randQueue
		return 0

tOpen = 900
lamda = 1
tClose = 1700
ap = AmusementPark()
time = Time()
tCurrent = 900
time.deconvertingTime(tCurrent, True)
qp = QuickPass(ap, time.getTime(), 100)
simulation = np.random.exponential(lamda, 500)
counter = 0

for i in range(len(simulation)):
	time.runtiming(simulation[i])
	quick = False
	if time.getTime() > tClose:
		break
	else:
		mustNQ = True if qp.getIndexAvailableTime(time.getTime()) == [] else False
		# print "Must : ", mustNQ
		if ap.chanceQuickPass() > qp.treshold or mustNQ:
			randQueue = ap.getIndexByTime(time.getTime())
			if ap.getShiftKuota(randQueue) > 1:
				ap.addQueue(randQueue)
			else:
				quick = True
				randQueue = qp.getTicket(time.getTime())
				if randQueue > 0:
					ap.addQueue(randQueue)
				else:
					print "Maaf waktu yang tersedia sudah tidak ada"
					break
		else:
			quick = True
			randQueue = qp.getTicket(time.getTime())
			if randQueue > 0:
				ap.addQueue(randQueue)
			else:
				print "Maaf waktu yang tersedia sudah tidak ada"
				break
	if quick == True:
		rtime = qp.getRangetime(randQueue)
		backrangetime = str(rtime['start'])+"-"+str(rtime['finish'])
	else:
		backrangetime = "-"
	print "Pengunjung ke- \t Waktu Kedatangan(Jam) \t Rentang Waktu kedatangan (Menit) \t Pilihan Antrian \t Interval Waktu Kembali \t Mulai Layanan \t Lama Waktu Antri(menit)"
	print i+1, "\t", "%0.f" % time.getTime(), "\t", "%2.f" % simulation[i], "\t", "Normal" if quick == False else "QuickPass", "\t", backrangetime, "\t", ap.getRuntime(randQueue), "\t", "%2.f" % ap.calcWaitingTime(randQueue, time.getTime()) if quick == False else "-"
	counter += 1

# print time.getTime()
print "==================="
print "Wahana tutup"
print "Jumlah Pengunjung Hari ini : ", counter