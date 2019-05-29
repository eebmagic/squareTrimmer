from PIL import Image


#######################################################
##### SETTINGS #####
# imagePATH = input("Drag file here: ").strip()
imagePATH = "OK_MUSIC.png"

GAP = 10
SQUARE = False
#######################################################

im = Image.open(imagePATH)
rawData = list(im.getdata())

# print(rawData[:10])
# print(im.size, im.size[0]*im.size[1], len(rawData))

### FIX DATA ###
fixedData = []
for point in rawData:
	one = round(point[0], -1)
	two = round(point[1], -1)
	new = [round(x-(x%30), -1) for x in point[:3]]
	fixedData.append(tuple(new))
	# print(point, new)
# exit()


### GET FREQUENCIES ###
freq = {}
for i, point in enumerate(fixedData[:len(fixedData)]):
	freq[point] = freq.get(point, 0) + 1

# print(freq)
# for i in sorted(freq, key=freq.get, reverse=True):
	# print(i, freq[i])

mostFreq = sorted(freq, key=freq.get, reverse=True)[0]

print(mostFreq)

Top, Bottom, Left, Right = None, None, None, None

outputData = []
for i, point in enumerate(fixedData):
	if point != mostFreq:
		Top = i
		outputData.append((104, 244, 66))
		#backGround.append(True)
		# break
	else:
		outputData.append(point)
		#backGround.append(False)

for i, point in enumerate(fixedData[::-1]):
	if point != mostFreq:
		Bottom = len(fixedData) - i
		break

print(Top, Bottom)

realData = []
for i, point in enumerate(outputData):
	if i == Top or i == Bottom:
		print("Fixed at: " + str(i))
		realData.append((0, 0, 0))
	else:
		realData.append(point)

outputData = realData[:]


print(outputData)
newIm = Image.new("RGB", im.size)
newIm.putdata(outputData)
newIm.save("Filtered.png")