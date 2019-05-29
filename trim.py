from PIL import Image
import sys
import os

def getMostFreq(inputList):
	frequencies = {}
	for i, val in enumerate(inputList):
		frequencies[val] = frequencies.get(val, 0) + 1
	return sorted(frequencies, key=frequencies.get, reverse=True)[0]

def topPos(inputList, ignorableItem):
	for i, point in enumerate(inputList):
		if point != ignorableItem:
			return i

def bottomPos(inputList, ignorableItem):
	for i, point in enumerate(inputList[::-1]):
		if point != ignorableItem:
			return len(inputList) - i

def leftPos(inputList, size, ignorableItem):
	for x in range(size[0]):
		for y in range(size[1]):
			index = (y * size[0]) + x
			if inputList[index] != ignorableItem:
				return index

def rightPos(inputList, size, ignorableItem):
	for x in range(size[0]):
		for y in range(size[1]):
			index = (y * size[0]) + (size[0]-x-1)
			if inputList[index] != ignorableItem:
				return index

def makeArray(inputList, size):
	return [inputList[i:i+size[0]] for i in range(0, len(inputList), size[0])]

def makeFlat(inputArray):
	output = []
	for row in inputArray:
		output = output + row
	return output

###########################################################################
### SETTINGS ###
PADDING = 5 
SQUARE = False
################################

##### START #####
### GET INPUT IMAGE ###
if len(sys.argv) > 1:
	IMAGE_PATH = sys.argv[1].strip()
	print(IMAGE_PATH)
else:
	IMAGE_PATH = input("Drag file here: ").strip()

if "-s" in sys.argv or "--s" in sys.argv:
	SQUARE = True

paddOptions = ["-p", "--p", "--padding"]
for option in paddOptions:
	if option in sys.argv:
		PADDING = int(sys.argv[sys.argv.index(option)+1])

### LOAD DATA ###
im = Image.open(IMAGE_PATH)
originalData = list(im.getdata())

### SIMPLIFY DATA ###
#make searchData
searchData = []
for point in originalData:
	newTup = [round(x-(x%30), -1) for x in point[:3]]
	searchData.append(tuple(newTup))

### FIND EDGE INDEXES ###
background = getMostFreq(searchData)
top = topPos(searchData, background)
bottom = bottomPos(searchData, background)
left = leftPos(searchData, im.size, background)
right = rightPos(searchData, im.size, background)

# Convert Edge pixels to Rows/Collumns #
edge = {
	"left": left%im.size[0],
	"right": right%im.size[0]+1,
	"top": int(top/im.size[0]),
	"bottom": int(bottom/im.size[0]+1)
}

### TRIM ###
asArray = makeArray(originalData, im.size)

# Adjust Edges to make square
if SQUARE:
	width = abs(edge["right"] - edge["left"])
	height = abs(edge["bottom"] - edge["top"])
	difference = abs(height - width)

	if width == height:
		pass
	
	elif min(width, height) == height:
		edge["bottom"] += difference/2
		edge["top"] -= difference/2
	
	elif min(width, height) == width:
		edge["left"] -= difference/2
		edge["right"] += difference/2


selection = []
for row in asArray:
	selection.append(row[int(edge["left"]-PADDING):int(edge["right"]+PADDING)])
selection = selection[edge["top"]-PADDING:edge["bottom"]+PADDING]


### SAVE ###
newSize = (int(edge["right"]-edge["left"]+(PADDING*2)), int(edge["bottom"]-edge["top"]+(PADDING*2)))
newIm = Image.new("RGB", newSize)
newIm.putdata(makeFlat(selection))
newIm.save("CROPPED.png")
exit("Image saved as: CROPPED.png")
