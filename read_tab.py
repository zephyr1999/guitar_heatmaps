# program to split up guitar tab into string and fret information
# note that with this program, i'm just getting individual note information,
# note note order or phrasing or any of that nonsense.

# Usage:  python read_tab.py [tab_file.txt] [graph_name]

import sys
import re
import numpy
import plotly.plotly as py
from plotly.graph_objs import *
import time

if (len(sys.argv) < 3):
	print ("Error: Not enough arguments.\n")
	print ("Usage:   python read_tab.py [tab_file.txt] [graph_name]")
	print ("Example: python read_tab.py lz_01.txt Get_the_led_out\n")
	sys.exit()

start_time = time.time()

regex = "[0-9]+"
infret = 0

#string data will hold all of the string fret info
#string 0 is high E, 1 is B, 2 is G, 3 is D, 4 is A, and 5 is low E
counts = numpy.zeros(shape = (6,25))

# first, get a list of each line
i = 5
with open(sys.argv[1], "r") as f:
	for l in f:
		# trim whitespace from the line
		line = l.strip()

		# TODO: Trim end of fretboard, maybe someone added text?
		#       example:
		#         |---------2----4-----4h5---|  text with numbers 1 21
		#                                These will get picked up ^ ^^

		# TODO: Check for 6 lines in a row, there could be additonal
		#       lines that start with '|' or '-' that would mess us up

		# check for the signature of a fretboard
		if len(line) > 0 and (line[0] == "|" or line[0] == "-"):
			# check if we're not already traversing a fretboard
			if infret == 0:
				# set infret flag to true
				infret = 1
			# check if we're already traversing a fretboard
			elif infret == 1:
				# increment string_data indexing
				i = i - 1
		# else outside fretboard
		else:       
			infret = 0
			i = 5
			continue

		# find all fret positions in the current string (line)
		frets = re.findall(regex, line)

		# check for empty string
		if (len(frets) == 0):
			continue

		# iterate the frets and append to string_data
		for fret in frets:
			normalFret = int(fret)
			normalFret = 24 if normalFret > 24 else normalFret
			counts[i][normalFret] = counts[i][normalFret] + 1
	
# use this for debugging 
#print counts
			
data = Data([
	Heatmap(
		z=counts,
		x=['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16',
			'17','18','19','20','21','22','23','24'],
		y=['E','A','D','G','B','e']
		)
	])

print("--- %s seconds ---" % (time.time() - start_time))

py.plot(data, filename=sys.argv[2])

						
					
				
				

	
