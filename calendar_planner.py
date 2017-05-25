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
parser.add_option("-o", "--output", dest="output")
parser.add_option("-s", "--sample", dest="sample", default=False, action="store_true")

kwargs, inputs = parser.parse_args()

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
		self.counted = True

	def __str__(self):
		return str(self.yyyymmdd)
	def __repr__(self):
		return str(self.yyyymmdd)


# We want to print calendar from Monday
# so if month starts midweek, we want to show previous days

WeekStart = 0 # Monday
WeekEnd = 6
deltaDays = 0
while (yyyymmdd_start - datetime.timedelta(deltaDays)).weekday() > 0:
	deltaDays += 1

yyyymmdd_actual_start = yyyymmdd_start - datetime.timedelta(deltaDays)
print yyyymmdd_actual_start

# same for month end - we want calendar until sunday


deltaDays = 0
while (yyyymmdd_end + datetime.timedelta(deltaDays)).weekday() < 6:
	deltaDays += 1
yyyymmdd_actual_end = yyyymmdd_end + datetime.timedelta(deltaDays)
print yyyymmdd_actual_end



days = []
daysIdx = 0
while True:
	thedate = yyyymmdd_actual_start + datetime.timedelta(daysIdx)
	if thedate > yyyymmdd_actual_end:
		break
	d = Day(thedate)
	if thedate < yyyymmdd_start:
		d.counted = False
	if thedate >= yyyymmdd_end:
		d.counted = False

	days.append( d )
	daysIdx+=1


# First week
daysIdx = 0
firstWeek = days[:7]

print firstWeek
# sys.exit(-1)


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


# print the day names
tr_start()
# td( "" )
for i in firstWeek:
	td( calendar.day_abbr[i.dateobj.weekday()], attrs={'class':'weekname'} )
tr_end()



# print calendar

idx = 0
for d in days:

	if d.dateobj.weekday() == WeekStart:
		tr_start()

	classes = ['aday']
	if d.isWeekend:
		classes.append('weekend')
	if d.counted:
		classes.append('counted')
	else:
		classes.append('notcounted')

	if idx + 1 < len(days):
		if days[idx].month != days[idx+1].month:
			classes.append('border-right')
	if idx + 7 < len(days):
		if days[idx].month != days[idx+7].month:
			classes.append('border-bottom')


	label = ""
	if d.day == 1 or d == days[0]:
		label += "<div style='float:left' class='monthname'>" + calendar.month_name[d.month] + "</div>"

		classes.append('monthname')

	label += str(d.day)



	td(label, attrs={'width':'100%', 'class':classes})


	if d.dateobj.weekday() == WeekEnd:
		tr_end()

	idx += 1




html('</table>')

html("""
<style type="text/css">

table {
	border-collapse:collapse;
	border:0;
	width:100%;
	height:100%;
	table-layout:fixed;
}
.d_weekend {
	background:#ccc;

}

td {
	padding:2px 3px;
	border:1px solid #bbb;
	font-family:"Helvetica Neue";
	
}

div.monthname {
	font-size:20px;
	margin-left:10px;
}
td.monthname {
	font-weight:normal !important;
}

td.aday {
	vertical-align:top;
	text-align:right;
	padding-right:10px;
	padding-top:10px;
	font-size:20px;
	font-weight:lighter;
	color:#333;
}
td.notcounted {
	background-color:#ccc !important;
}
td.weekname {
	vertical-align:middle;
	text-align:center;
	font-size:20px;
	font-weight:lighter;
	border:0;
	height:50px;
}
td.counted {
	color:#000;
	background-color:#fff;
}
td.weekend {
	background-color:#f0f0f0;
}
td.border-right {
	border-right:2px solid #aaa !important;
}
td.border-bottom {
	border-bottom:2px solid #aaa !important;
}
body * {
	font-size: 12px;
	font-family:"Helvetica Neue"
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

fn = "output.html"

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
