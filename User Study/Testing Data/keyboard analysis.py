import json
import statistics

files = range(1, 10)
directory = "Keyboard/"

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
		"word_jump_left": 0,
		"word_jump_right": 0,
		"bol": 0,
		"eol": 0,
		"text_top": 0,
		"text_bottom": 0,
		"ArrowLeft": 0,
		"ArrowRight": 0,
		"ArrowUp": 0,
		"ArrowDown": 0,
		"time": 0
	}

	for j in data[i]:
		if j[1][0]:
			if j[1][0] in d.keys():
				d[j[1][0]] += 1
			d["time"] = (j[2] - times[i])/60/1000

	pressData.append(d)

#for i in pressData:
#	print(i)

strokes = []
time = []
for i in pressData:
	s = 0
	for j in i.keys():
		if j == "time":
			time.append(i[j])
		else:
			s += i[j]
	strokes.append(s)

print("Time ", statistics.mean(time), ' +- ', statistics.stdev(time))
print("Strokes ", statistics.mean(strokes), ' +- ', statistics.stdev(strokes))