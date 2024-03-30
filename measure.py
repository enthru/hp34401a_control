import serial
import sys
import time
import csv
from datetime import datetime
import os

import matplotlib.pyplot as plt


def write_to_csv(filename, data):
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def read_from_csv(filename):
    numbers = []
    times = []
    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            numbers.append(float(row[0]))
            times.append(datetime.strptime(row[1], '%H:%M:%S'))
    return numbers, times

def clear_csv(filename):
    if os.path.exists(filename):
        with open(filename, 'w', newline=''):
            pass

if len(sys.argv)<3:
	print ("""
Not enough arguments.

Usage:

measure.py <typeof measure> <range> <resolution> <round digits> <mesure count>
""")
	sys.exit(0)
ser = serial.Serial(sys.argv[1], 9600)
ser.write(bytearray('*idn?\r\n','ascii'))

bs = ser.readline()
print(bs.decode('ascii'))

clear_csv('data.csv')

if sys.argv[2] == "dc":
	print("Measuring DC:")
	ser.write(bytearray('syst:rem;\r\n','ascii'))
	i = 0
	while i<int(sys.argv[6]):
		i = i + 1
		ser.write(bytearray(':meas:volt:dc? '+ sys.argv[3] + ',' + sys.argv[4] + ';\r\n','ascii'))
		bs = ser.readline()
		current_time = datetime.now().strftime('%H:%M:%S')
		data = [round(float(bs.decode('ascii')),int(sys.argv[5])), current_time]
		print(data)
		write_to_csv('data.csv', data)
		time.sleep(1)
elif sys.argv[2] == "ac":
	print("Measuring AC:")
	ser.write(bytearray('syst:rem;\r\n','ascii'))
	i = 0
	while i<int(sys.argv[6]):
		i = i + 1
		ser.write(bytearray(':meas:volt:ac? '+ sys.argv[3] + ',' + sys.argv[4] + ';\r\n','ascii'))
		bs = ser.readline()
		current_time = datetime.now().strftime('%H:%M:%S')
		data = [round(float(bs.decode('ascii')),int(sys.argv[5])), current_time]
		print(data)
		write_to_csv('data.csv', data)
		time.sleep(1)
            		
numbers, times = read_from_csv('data.csv')
plt.plot(times, numbers, marker='o')
plt.xlabel('Время')
plt.ylabel('Число')
plt.title('График значений')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('graph.png') 
plt.show()
