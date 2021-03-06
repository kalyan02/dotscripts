import datetime
import calendar
import json
import sys

from optparse import OptionParser
parser = OptionParser()

# indicate start date and days
parser.add_option("-d", "--day", dest="day", default=1)
parser.add_option("-m", "--month", dest="month")
parser.add_option("-y", "--year", dest="year")
parser.add_option("-D", "--days", dest="days")
parser.add_option("-M", "--months", dest="months")

parser.add_option("-t", "--title", dest="title")
parser.add_option("-i", "--input", dest="input")
parser.add_option("-o", "--output", dest="output")
parser.add_option("-s", "--sample", dest="sample", default=False, action="store_true")

kwargs, inputs = parser.parse_args()

if kwargs.sample:
    s = []
    for i in range(3):
        grp = {
                "name" : "Group Name %d" % i,
                "sub" : []
                }
        for j in range(8):
            grp["sub"].append( "Sub-item %d" % j )
        s.append( grp )

    fh = open("sample.json", "w+")
    fh.write( json.dumps( s, indent=4 ) )
    fh.close()
    print "Generated sample.json"
    sys.exit(0)

if not kwargs.input:
	parser.error("--input | -i : input JSON file is required")

if kwargs.output:
    if not kwargs.output.endswith(".html"):
        parser.error("--output | -o : output needs to have HTML file extension")

if not kwargs.title:
	parser.error("--title | -t : title is required")

# either today or exact start date
try:
	year = int(kwargs.year)
	month = int(kwargs.month)
	day = int(kwargs.day)
except:
	if kwargs.day == "today":
		d = datetime.date.today()
		day, month, year = d.day, d.month, d.year
	else:

		if not kwargs.month:
			parser.error("--month | -m : month is required (January:1; December:12)")

		if not kwargs.year:
			parser.error("--year | -y : year is required (eg: 2016)")

		parser.error("Invalid month or year passed")


# default start is beginning of month
yyyymmdd_start = datetime.date(year,month,day)

nmonths = 1

# either end of month or end of next month
if kwargs.months:
	try:
		# default is 1 month
		nmonths = int(kwargs.months)
		print "nomont", nmonths
	except:
		nmonths = 1

# end of this month
if nmonths == 1:
	# default end is end of month
	yyyymmdd_end = datetime.date(year,month,1) + datetime.timedelta(calendar.monthrange(year,month)[1])
else:
	daysIdx = 0
	nMonthsChanged = 0
	currentMonth = yyyymmdd_start.month

	# Loop until number of months change
	while True:
		thedate = yyyymmdd_start + datetime.timedelta(daysIdx)
		if thedate.month != currentMonth:
			currentMonth = thedate.month
			nMonthsChanged += 1

		if nMonthsChanged >= nmonths:
			break

		daysIdx += 1

	yyyymmdd_end = thedate


# unless specified
if kwargs.days:
	try:
		ndays = int(kwargs.days)
	except:
		parser.error("--days | -n : Number of days need to be specified")

	yyyymmdd_end = yyyymmdd_start + datetime.timedelta(ndays)

	
print yyyymmdd_start
print yyyymmdd_end

# sys.exit(-1)

if kwargs.input:
	try:
		fh = open(kwargs.input,'r')
		categories = json.load(fh)
		fh.close()
	except Exception, e:
		parser.error("error loading json from input file." + str(e))





class Day(object):
	def __init__(self, yyyymmdd):
		if type(yyyymmdd) == datetime.date:
			yyyymmdd = (yyyymmdd.year, yyyymmdd.month, yyyymmdd.day)

		self.yyyymmdd = yyyymmdd
		self.dateobj = datetime.date(*yyyymmdd)
		self.isWeekend = self.dateobj.weekday() >= 5
		self.isWeekday = self.dateobj.weekday() < 5
		self.name = calendar.day_abbr[ self.dateobj.weekday() ][:2]
		self.day = yyyymmdd[2]
		self.month = yyyymmdd[1]


days = []
daysIdx = 0


while True:
	thedate = yyyymmdd_start + datetime.timedelta(daysIdx)
	if thedate >= yyyymmdd_end:
		break
	days.append( Day(thedate) )
	daysIdx+=1


thehtml = ''
def html(h):
	global thehtml
	thehtml += h

def htmlTag(tag, content, attrs={}):
	global thehtml
	attrsHtml = []
	for k, v in attrs.items():
		if k == 'class' and type(v) == list:
			v = " ".join(v)

 		attrsHtml.append( "%s=\"%s\"" % (k,v) )
	thehtml += "<%s %s>%s</%s>" % (tag, " ".join(attrsHtml), content, tag)

def tr_start():
	html('<tr>')

def tr_end():
	html('</tr>')

def td(c='', attrs={}):
	htmlTag('td', c, attrs)

html('<table border=0>')


# print the month names
tr_start()

td( "", {"colspan":2, "class":"thetitle"} )
currmonth = days[0].month
monthspanlist = [ currmonth ]
monthspans = [ 0 ]
for day in days:
	if day.month != currmonth:
		monthspans.append(0)
		monthspanlist.append(day.month)
		currmonth = day.month

	monthspans[-1] += 1

for m, s in zip(monthspanlist,monthspans):
	td(calendar.month_name[ m ], {"colspan": s, "class":"dateitem" })
tr_end()


# print the day of the month names
tr_start()
h = "%s" % (kwargs.title)

td( h, {"colspan":2, "class":"thetitle"} )
for day in days:
	c = ['dateitem']
	if day.isWeekend:
		c.append('d_weekend')
	td(day.name, {"class":c})
tr_end()

# print the day of the month numbers
tr_start()
td( '', {"colspan":2, "class":"thetitle"} )
for day in days:
	c = ['dateitem']
	if day.isWeekend:
		c.append('d_weekend')
	td(day.day, {"class":c})
tr_end()


# print all crap
for eachCategory in categories:
	
	nSubs = len(eachCategory["sub"])
	for cIdx in range(nSubs):
		tr_start()
		# generate the category header on  the left
		if cIdx == 0:
				td(eachCategory['name'], {"rowspan":nSubs, "class":"catitem", "valign":"top"})

		eachSub = eachCategory['sub'][cIdx]

		# then stuff in sub-category name
		td(eachSub, {"class":"subitem"})

		# date range
		for day in days:
			c = ['dateitem']
			if day.isWeekend:
				c.append('d_weekend')
			td('&nbsp;', {"class":c})

		tr_end()

	tr_start()
	# td('&nbsp;', {"colspan":50, "class":"rowspacer"})
	td('&nbsp;', {"colspan":2, "class":"rowspacer"})


	for s in monthspans:
		td("&nbsp;", {"colspan": s, "class":"dateitem" })

	tr_end()



html('</table>')

html("""
<style type="text/css">
.dateitem {
	width:25px;
	border:1px solid black;
	text-align:center;
}
.catitem {
	text-align:right;
	width:80px;
}
.subitem {
	border:1px solid black;
	text-align:right;
	width:220px;
}
table {
	border-collapse:collapse;
	border:0;
}
.d_weekend {
	background:#ccc;
}
td {
	padding:2px 3px;
}
body * {
	font-size: 12px;
	font-family:"Arial"
}
.thetitle {
	text-align:left;
	padding-left:20px;
	font-weight:bold;
}
.rowspacer {
	
}
</style>
""")

fn = kwargs.input.replace(".json", ".html")

if kwargs.output:
    fn = kwargs.output

try:
    fh = open(fn, "w+")
    fh.write(thehtml)
    fh.close()
    print "Output written to %s" % fn
    sys.exit(0)
except Exception, e:
    print "Error writing to %s" % fn
    print e
    sys.exit(0)

print thehtml
