import json
import statistics

files = range(1, 13)
directory = "KeySlide/"

data = []
times = []
for i in files:
	try:
		f = open(directory + str(i) + "/data.txt", 'r')
		content = json.loads(f.read())
		data.append(content)
		f.close()

		f = open(directory + str(i) + "/user.txt", 'r')
		content = int(f.read())
		times.append(content)
		f.close()
	except:
		continue

pressData = []

for i in range(len(data)):
	d = {
		"stroke_secondary": 0,
		"stroke_primary": 0,
		"time": 0
	}

	for j in data[i]:
		if j[0] in d.keys():
			d[j[0]] += 1
		d["time"] = (j[2] - times[i])/60/1000

	pressData.append(d)

#for i in pressData
#	print(i)

primary = []
secondary = []
time = []
for i in pressData:
	time.append(i["time"])
	primary.append(i["stroke_primary"])
	secondary.append(i["stroke_secondary"])

print("Time ", statistics.mean(time), ' +- ', statistics.stdev(time))
print("Primary ", statistics.mean(primary), ' +- ', statistics.stdev(primary))
print("Secondary ", statistics.mean(secondary), ' +- ', statistics.stdev(secondary))