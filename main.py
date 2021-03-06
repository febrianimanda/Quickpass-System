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
			return True
		else :
			print "Maaf yang anda pilih sudah tidak tersedia"
			return False

	def getKuota(self):
		return self.kuota

	def getIndexByTime(self, time):
		for i in xrange(len(self.runtime)):
			if time < self.runtime[i]:
				return i

	def calcWaitingTime(self, indexRuntime, time):
		return self.getRuntime(indexRuntime) - time

class QuickPass:
	def __init__(self, park, tCurrent, percentage):
		self.rangetime = {}
		self.availabletime = []
		self.treshold = 0.2
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
			randQueue = random.choice(avatime)
			# print "rand get ticket:", randQueue
			self.addQueue(randQueue)
			return randQueue
		return 0

def main(qp, ap, time, x):
	counter = 0
	with open('results31-'+str(x)+'.csv', 'w') as csvfile:
		fieldnames = ['Pengunjung Ke-', 'Waktu Kedatangan (Jam)', 'Rentang Waktu Kedatangan (Menit)', 'Pilihan Antrian', 'Interval Waktu Kembali', 'Mulai Layanan', 'Lama Waktu Antri (Menit)']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for i in range(len(simulation)):
			time.runtiming(simulation[i])
			quick = False
			canPlay = True
			if time.getTime() > tClose:
				break
			else:
				mustNQ = True if qp.getIndexAvailableTime(time.getTime()) == [] else False
				chance = ap.chanceQuickPass()
				if chance > qp.treshold or mustNQ:
					randQueue = ap.getIndexByTime(time.getTime())
					avakuota = ap.getShiftKuota()
					if avakuota.get(randQueue) > 0:
						ap.addQueue(randQueue)
					else:
						quick = True
						randQueue = qp.getTicket(time.getTime())
						print randQueue
						if randQueue != 0:
							if ap.addQueue(randQueue) == False:
								canPlay = False
						else:
							canPlay = False
				else:
					quick = True
					randQueue = qp.getTicket(time.getTime())
					print randQueue
					if randQueue != 0:
						if ap.addQueue(randQueue) == False:
								canPlay = False
					else:
						canPlay = False
			if canPlay:
				if quick == True:
					rtime = qp.getRangetime(randQueue)
					backrangetime = str(rtime['start'])+"-"+str(rtime['finish'])
				else:
					backrangetime = "-"
			print "Pengunjung ke- \t Waktu Kedatangan(Jam) \t Rentang Waktu kedatangan (Menit) \t Pilihan Antrian \t Interval Waktu Kembali \t Mulai Layanan \t Lama Waktu Antri(menit)"
			if canPlay:
				print i+1, "\t", "%0.f" % time.getTime(), "\t", "%2.f" % simulation[i], "\t", "Normal" if quick == False else "QuickPass", "\t", backrangetime, "\t", ap.getRuntime(randQueue), "\t", "%2.f" % ap.calcWaitingTime(randQueue, time.getTime()) if quick == False else "-"
				writer.writerow({'Pengunjung Ke-': i+1, 'Waktu Kedatangan (Jam)': "%0.f" % time.getTime(), 'Rentang Waktu Kedatangan (Menit)': "%2.f" % simulation[i], 'Pilihan Antrian':"Normal" if quick == False else "QuickPass", 'Interval Waktu Kembali':backrangetime, 'Mulai Layanan':ap.getRuntime(randQueue), 'Lama Waktu Antri (Menit)':"%2.f" % ap.calcWaitingTime(randQueue, time.getTime()) if quick == False else "-"})
				counter += 1
			else:
				print i+1, "\t", "%0.f" % time.getTime(), "\t", "%2.f" % simulation[i], "\t", "-", "\t", '-', "\t", '-', "\t", "-"
				writer.writerow({'Pengunjung Ke-': i+1, 'Waktu Kedatangan (Jam)': "%0.f" % time.getTime(), 'Rentang Waktu Kedatangan (Menit)': "%2.f" % simulation[i], 'Pilihan Antrian':"-", 'Interval Waktu Kembali':'-', 'Mulai Layanan':'-', 'Lama Waktu Antri (Menit)':"-"})

	print ""
	print "Wahana tutup"
	print "Jumlah Pengunjung Hari ini : ", counter
	return counter

tOpen = 900
lamda = 1
tClose = 1700
ap1 = AmusementPark()
ap2 = AmusementPark()
ap3 = AmusementPark()
time = Time()
time2 = Time()
time3 = Time()

tCurrent = 900
time.deconvertingTime(tCurrent, True) #time initialization
time2.deconvertingTime(tCurrent, True) #time initialization
time3.deconvertingTime(tCurrent, True)

simulation = np.random.exponential(lamda, 300) #simulation initialization
qp1 = QuickPass(ap1, time.getTime(), 40) #QP initialization with 100% acceptance
qp2 = QuickPass(ap2, time2.getTime(), 65)
qp3 = QuickPass(ap3, time3.getTime(), 100)

c1 = main(qp1, ap1, time, 1)
c2 = main(qp2, ap2, time2, 2)
c3 = main(qp3, ap3, time3, 3)


with open("Output31.txt", "w") as text_file:
	text_file.write("Kapasitas Quickpass 1: {} \n".format(qp1.kuotapercentage))
	text_file.write("Jumlah Pengunjung yang ditangani: {} \n".format(c1))
	text_file.write("Kuota tersisa: {} \n\n".format(ap1.shiftkuota))
	
	text_file.write("Kapasitas Quickpass 2: {} \n".format(qp2.kuotapercentage))
	text_file.write("Jumlah Pengunjung yang ditangani: {} \n".format(c2))
	text_file.write("Kuota tersisa: {} \n\n".format(ap2.shiftkuota))
	
	text_file.write("Kapasitas Quickpass 3: {} \n".format(qp3.kuotapercentage))
	text_file.write("Jumlah Pengunjung yang ditangani: {} \n".format(c3))
	text_file.write("Kuota tersisa: {} \n".format(ap3.shiftkuota))

print ""
print "================"
print ""
print "Jumlah Pengunjung dengan QP 40% : ", c1
print "Jumlah Pengunjung dengan QP 65% : ", c2
print "Jumlah Pengunjung dengan QP 90% : ", c3