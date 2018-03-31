import numpy as np
import pandas as pd
from ttc import Student, Market

datadir = "./data/"
filename = "b1_rooming"

df = pd.read_csv(datadir+filename+".csv")
df = df.replace(np.nan, '')
data = df.values

priority = []
for row in data:
	name = row[0]
	endowment = row[1] if row[1] else None
	prefs = row[2:]
	prefs = [p for p in prefs if p]
	s = Student(name, endowment, prefs)
	priority.append(s)

## Setup the market
rooms = [
"141H",
"133A",
"151B",
"122C",
"101A"
]

# abhi = Student("Abhi", "141H", ["133A","122C","141H"])
# pat = Student("Pat", "133A", ["151B","133A"])
# bgu = Student("Bgu", "151B", ["133A", "141H", "151B"])
# mich = Student("Michael", "122C", ["101A","122C"])
# phil = Student("Phil", None, ["141H"])

# priority = [abhi, mich, bgu, pat, phil]

m = Market("Burton 1", priority, rooms)


## Validate and fill in prefs for newcomers
print "MARKET VALID?\n%s\n" % m.is_valid()
m.fill_prefs()
print m


## Run YRMH-IGYT
allocation, log = m.yrmh_igyt()


## Print results
print '{:10s} {:s}\t\t>=\t{:s}'.format("STUDENT", "NEW", "ORIGINAL")
print "----------------------------------"
for student in priority:
	print '{:10s} {:s}\t\t>=\t{:s}'.format(student.name, allocation[student], student.endowment)

print "\nINCENTIVE-COMPATIBLE?\n%s\n" % m.is_IR(allocation)

print "LOG\n------------------------------------\n%s" % log
