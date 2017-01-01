#!/usr/bin/python

from PIL import Image
import os
import sys
import glob
from optparse import OptionParser
args = sys.argv

parser = OptionParser()
parser.add_option("-o", "--output", dest="output")
parser.add_option("-s", "--size", dest="size")
parser.add_option("-d", "--debug", dest="debug", action="store_true")
parser.add_option("-m", "--move", dest="move", action="store_true") #todo
parser.add_option("-r", "--reverse", dest="reverse", action="store_true")
kwargs, inputs = parser.parse_args()

if len(inputs) < 2:
	print "Error: required atleast 2 images"
	sys.exit(-1)

if not kwargs.size:
	output_size = 1600
	print "Resizing to width (%s)" % output_size
else:
	output_size = int(kwargs.size)

if kwargs.output and os.path.exists(kwargs.output):
	output_dir = kwargs.output
else:
	output_dir = "."

if kwargs.debug:
	DEBUG = True
else:
	DEBUG = False

spacing = 10

images = []
min_height = 999999

# reverse if required
if kwargs.reverse:
	inputs = inputs[::-1]

##############################################################################
# create a composite name
##############################################################################

def equal_substrs(items, l):
	k = items[0]
	for i in range (1,len(items)):
		each = items[i]
		if each[:l] != k[:l]:
			return False
	return True


fnames = map( os.path.basename, inputs )

common_chars = ''
short_ids = []
idx = 0
max_idx = min(map(len, fnames))

while True:
	if equal_substrs(fnames,idx+1):
		idx += 1
	else:
		break

short_ids = map(lambda x: x[idx:], fnames)
short_ids = map(lambda x: x[0:x.rindex(".")], short_ids)

#  AAX.jpg and AAY.JPG -> AA_X_Y.jpg
output_name = fnames[0][:idx] + "_" + "_".join(short_ids) + ".jpg"

##############################################################################
# read from disk
##############################################################################


original_sizes = []
for each in inputs:
	b_name = os.path.basename(each)
	img = Image.open(each)
	images.append(img)

	w, h = img.size
	original_sizes.append( img.size )
	if min_height > h:
		min_height = h


##############################################################################
# scale evenly to match the heights
##############################################################################

scaled_sizes = []
for img in images:
	w, h = img.size
	scale_factor = 1.0 * min_height / h
	scaled_w, scaled_h = w * scale_factor, h * scale_factor
	scaled_sizes.append( (scaled_w,scaled_h) )

scaled_width = sum(map(lambda x:x[0], scaled_sizes))

##############################################################################
# if the even scaled size is greater, then further downscale the images
##############################################################################

if DEBUG:
	print "%20s %s" % ("original", original_sizes)
	print "%20s %s" % ("equal sized", scaled_sizes)

output_size_nospace = output_size - (len(images)-1)*spacing

if scaled_width > output_size_nospace:
	scaled_sizes = []
	for img in images:
		w, h = img.size

		scale_factor = (1.0 * min_height / h) * (1.0 * output_size_nospace/scaled_width)
		if DEBUG:
			print "factor", scale_factor, min_height, h, output_size_nospace, scaled_width
		scaled_w, scaled_h = w * scale_factor, h * scale_factor
		scaled_sizes.append( (int(scaled_w),int(scaled_h)) )
else:
	print "output size is too big. can't upscale"
	sys.exit(-1)


if DEBUG:
	print "%20s %s" % ("expected size", scaled_sizes)

##############################################################################
# layout in final image
##############################################################################

scaled_width = sum(map(lambda x:x[0], scaled_sizes))
scaled_height = scaled_sizes[0][1]

# using output size as it includes spacing. 
# scaled_width does not have spacing/padding
dest = Image.new("RGB", (output_size, scaled_height), color=(255,255,255) )

x_offset = 0
y_offset = 0
idx = 0
if DEBUG:
	print images,scaled_sizes
for img, size in zip(images,scaled_sizes):
	w, h = size
	# now resize original image first
	imgr = img.resize( size, Image.ANTIALIAS )
	# paste resized image into dest
	dest.paste( imgr, (x_offset,y_offset) )
	# spacing
	x_offset += w + spacing


dest_fn = output_dir.rstrip('/') + "/" + output_name

dest.save(dest_fn, format='JPEG')

print "Generating", output_name


