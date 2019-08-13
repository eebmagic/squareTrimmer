from PIL import Image
import sys
import os
from pathlib import Path


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
			index = (y * size[0]) + (size[0] - x - 1)
			if inputList[index] != ignorableItem:
				return index


def makeArray(inputList, size):
	return [inputList[i:i + size[0]] for i in range(0, len(inputList), size[0])]


def makeFlat(inputArray):
	output = []
	for row in inputArray:
		output = output + row
	return output


###########################################################################
# SETTINGS #
PADDING = 5
SQUARE = False
###########################################################################

# START #
# GET INPUT IMAGE AND OPTIONS #
if len(sys.argv) > 1:
	IMAGE_PATH = sys.argv[1].strip()
else:
	IMAGE_PATH = input("Drag file here: ").strip()

if "-s" in sys.argv or "--s" in sys.argv:
	SQUARE = True

# Padding option
paddOptions = ["-p", "--p", "--padding"]
for option in paddOptions:
	if option in sys.argv:
		try:
			PADDING = int(sys.argv[sys.argv.index(option) + 1])
		except IndexError:
			quit(f"""\n### ERROR: No padding input was given after the {option} flag.
Input must be a number of pixels for border.""")

# Ouput file option
if '-o' in sys.argv[1:]:
	output_file_name = sys.argv[sys.argv[1:].index('-o') + 2]
	if not output_file_name.endswith('.png'):
		output_file_name += '.png'
else:
	output_file_name = None

# LOAD DATA #
im = Image.open(IMAGE_PATH)
originalData = list(im.getdata())

# SIMPLIFY DATA #
# make searchData
searchData = []
for point in originalData:
	newTup = [round(x - (x % 30), -1) for x in point[:3]]
	searchData.append(tuple(newTup))

# FIND EDGE INDEXES #
background = getMostFreq(searchData)
top = topPos(searchData, background)
bottom = bottomPos(searchData, background)
left = leftPos(searchData, im.size, background)
right = rightPos(searchData, im.size, background)

# Convert Edge pixels to Rows/Collumns #
edge = {
	"left": left % im.size[0],
	"right": right % im.size[0] + 1,
	"top": int(top / im.size[0]),
	"bottom": int(bottom / im.size[0] + 1)
}

# TRIM #
asArray = makeArray(originalData, im.size)

# Adjust Edges to make square
if SQUARE:
	width = abs(edge["right"] - edge["left"])
	height = abs(edge["bottom"] - edge["top"])
	difference = abs(height - width)

	if width == height:
		pass

	elif width > height == height:
		edge["bottom"] += difference / 2
		edge["top"] -= difference / 2

	else:
		edge["left"] -= difference / 2
		edge["right"] += difference / 2


selection = []
for row in asArray:
	left_edge = int(edge["left"] - PADDING)
	if left_edge < 0:
		left_edge = 0

	right_edge = int(edge["right"] + PADDING)
	if right_edge > im.size[0]:
		right_edge = im.size[0]

	selection.append(row[left_edge:right_edge])

top_edge = edge["top"] - PADDING
if top_edge < 0:
	top_edge = 0

bottom_edge = edge["bottom"] + PADDING
if bottom_edge > im.size[1]:
	bottom_edge = im.size[1]

selection = selection[top_edge:bottom_edge]


# SAVE #
new_x = int(right_edge - left_edge)
new_y = int(bottom_edge - top_edge)
newSize = (new_x, new_y)
newIm = Image.new("RGB", newSize)
newIm.putdata(makeFlat(selection))

if not output_file_name:
	output_file_name = input("\n\tWhat do you want to name the output file?: ")
	if not output_file_name.endswith('.png'):
		output_file_name += '.png'

OUTPUT_PATH = os.getcwd() + "/" + output_file_name
newIm.save(OUTPUT_PATH)
exit("Image saved as: " + OUTPUT_PATH)
