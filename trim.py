from PIL import Image

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
SQUARE = True
################################

##### START #####

### LOAD DATA ###
im = Image.open("Filtered.png")
rawData = list(im.getdata())

### SIMPLIFY DATA ###

### FIND EDGE INDEXES ###
background = getMostFreq(rawData)
top = topPos(rawData, background)
bottom = bottomPos(rawData, background)
left = leftPos(rawData, im.size, background)
right = rightPos(rawData, im.size, background)

# Convert Edges to Row/Collumns #
edge = {
	"left": left%im.size[0],
	"right": right%im.size[0]+1,
	"top": int(top/im.size[0]),
	"bottom": int(bottom/im.size[0]+1)
}

### TRIM ###
asArray = makeArray(rawData, im.size)

selection = []
for row in asArray:
	selection.append(row[edge["left"]-PADDING:edge["right"]+PADDING])
selection = selection[edge["top"]-PADDING:edge["bottom"]+PADDING]


### SAVE ###
newSize = (edge["right"]-edge["left"]+(PADDING*2), edge["bottom"]-edge["top"]+(PADDING*2))
newIm = Image.new("RGB", newSize)
newIm.putdata(makeFlat(selection))
newIm.save("CROPPED.png")
