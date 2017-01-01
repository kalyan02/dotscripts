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
parser.add_option("-i", "--ignore-existing", dest="ie")
kwargs, inputs = parser.parse_args()

output_dir = kwargs.output
size = kwargs.size
ignore_existing = kwargs.ie

if not size:
    size = '1280'

if not output_dir:
    output_dir = 'r'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)


is_percent = '%' in size
dest_w, dest_h = None, None
if '%' in size:
	dest_w = size.strip().strip('%').strip()
	try:
		dest_w = int(dest_w)
	except:
		print "Error, need proper size format"
		print "Format: --size=10%"
		sys.exit(-1)

if 'x' in size:
	dest_w, dest_h = size.split('x')
	print dest_w, dest_h

if not dest_w or not dest_h:
	if not is_percent:
		try:
			dest_w = int(size)
		except:
			print "Error, need proper size"
			print "Possible options format: =100x100, =100, =50%" 
			sys.exit(-1)

if not os.path.exists(output_dir):
	print "Need a valid existing directory"
	sys.exit(-1)

for each in inputs:
    b_name = os.path.basename(each)
    dest_fn = output_dir.rstrip('/') + "/" + b_name

    if ignore_existing:
        if os.path.exists(dest_fn):
            print 'Skipping:', each
            continue

    img = Image.open(each)
    
    resize_mode = Image.ANTIALIAS
    imgr = None
    if is_percent:
		osize = img.size
		imgr = img.resize( (osize[0]*dest_w/100, osize[0]*dest_w/100), resize_mode )
	#elif dest_w and dest_h:
	#	# todo, need to fit it to bounding box
	#	pass
    elif dest_w:
        osize = img.size
        _w, _h = dest_w, osize[1] * dest_w / osize[0]
        imgr = img.resize( (_w,_h), resize_mode )
	

    b_ext = b_name.split('.')[-1]
    if b_ext.upper() == 'JPG':
		b_ext = 'JPEG'
    
    imgr.save( dest_fn, format=b_ext )
    print 'Resizing:', each 
