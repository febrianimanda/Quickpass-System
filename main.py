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
				self.initTime(temp[0] + temp[1], temp[2] + temp[3])
			else:
				return temp[0] + temp[1], temp[2] + temp[3]
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

	def getShiftKuota(self, index):
		return self.shiftkuota[index]

	def initAllPlayingTime(self):
		for i in data:
			self.runtime[i] = data[i]['play']

	def getRuntime(self):
		return self.runtime

	def checkAvailableKuota(self, index):
		return True if self.getShiftKuota(index) > 0 else False

	def addQueue(self, index):
		if self.checkAvailableKuota(index):
			self.kuota[index] = self.kuota[index] - 1
		else :
			print "Maaf yang anda pilih sudah tidak tersedia"

	def getKuota(self):
		return self.kuota

	def getIndexByTime(self, time):
		for i in range(len(self.rangetime)):
			if time < self.rangetime[i]:
				return i

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
				index.append(i)
		return index

	def showAvailableShift(self, park):
		for i in self.availabletime:
			if park.checkAvailableKuota(i):
				print i, '|', self.rangetime[i]['start'], '-', self.rangetime[i]['finish'], '|', park.getShiftKuota(i)

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

	def getRangetime(self):
		return self.rangetime

tOpen = 900
lamda = 1
tClose = 1700
ap = AmusementPark()
time = Time()
tCurrent = 900
time.deconvertingTime(tCurrent, True)
qp = QuickPass(ap, time.getTime(), 100)
simulation = np.random.exponential(lamda, 500)

print ap.getRuntime()
print qp.getRangetime()
print qp.getIndexAvailableTime(time.getTime())
qp.addQueue(14)
print qp.getQueue()
quit()

for i in range(len(simulation)):
	if time.getTime() > tClose:
		break
	else:
		if ap.chanceQuickPass() > qp.treshold:
			ap.addQueue()
		else:
			ava = qp.getIndexAvailableTime(time.getTime())

		time.runtiming(simulation[i])
		print i,'-',
		if time.getHour < 10:
			print '0',time.getHour(),':',time.getMinutes()
		else:
			print time.getHour(),':',time.getMinutes()

print "Maaf wahana sudah tutup"
print "Pengunjung ke- \t Waktu Kedatangan(Jam) \t Rentang Waktu kedatangan (Menit) \t Pilihan Antrian \t Interval Waktu Kembali \t Mulai Layanan \t Lama Waktu Antri \t Nomor Antrian"