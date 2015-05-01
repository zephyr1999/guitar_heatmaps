# program to split up guitar tab into string and fret information
# note that with this program, i'm just getting individual note information,
# note note order or phrasing or any of that nonsense.

import numpy
import plotly.plotly as py
from plotly.graph_objs import *
import re

filename = "lz_01.txt"
regex = "[0-9]+"
infret = 0

#string data will hold all of the string fret info
#string 0 is high E, 1 is B, 2 is G, 3 is D, 4 is A, and 5 is low E
string_data = [[],[],[],[],[],[]]

# first, get a list of each line
j = 0
with open(filename, "r") as f:
    for line in f:

      # TODO: Trim whitespace from front of line, 
      #       line[0] will fail in some cases unless we do this.
      #       example:          v------- start of tab
      #    start of page  ->    |----

      # TODO: Trim end of fretboard, maybe someone added text?
      #       example:
      #         |---------2----4-----4h5---|  text with numbers 1 21
      #                                These will get picked up ^ ^^

      # check for the begining of a fretboard
      if line[0] == "|" and infret == 0:
        # set infret flag to true
        infret = 1
      # else if check for the internal of a fretboard
      elif (line[0] == "|" or line[0] == "-") and infret == 1:
        # increment string_data indexing
        j = j + 1
      # else outside fretboard
      else:       
        infret = 0
        j = 0
        continue

      # find all fret positions in the current string (line)
      frets = re.findall(regex, line)

      # check for empty string
      if (len(frets) == 0):
        continue

      # iterate the frets and append to string_data
      for fret in frets:
        string_data[j].append(int(fret))
    
# now string data is a list of fret info, indexed by string number
# I need to create a 6x24 matrix of counts
counts = numpy.zeros(shape = (6,25))

for i in range(len(string_data)):
  for j in range(len(string_data[i])):
    # stupidity check because some tab uses numbers > 24
    if string_data[i][j] > 24:
      counts[i][24] = counts[i][24] + 1
    else:
      counts[i][string_data[i][j]] = counts[i][string_data[i][j]] + 1
      
#ploting like this will result in the heatmap being flipped, i.e. high E string on bottom
# and low E string on top

flipped_counts = numpy.zeros(shape = (6,25))

flipped_counts[0] = counts[5]
flipped_counts[1] = counts[4]
flipped_counts[2] = counts[3]
flipped_counts[3] = counts[2]
flipped_counts[4] = counts[1]
flipped_counts[5] = counts[0]

# use this for debugging 
#print flipped_counts

# this is the total number of notes
# using two checks to make sure no data is lost in translation
# a uses note counts per string(flipped counts) and b uses length of note lists (string_data)
a=[]
for i in flipped_counts: a.append(sum(i))
print sum(a)
b=[]
for i in string_data: b.append(len(i))
print sum(b)
      
data = Data([
  Heatmap(
    z=flipped_counts,
    x=['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16',
      '17','18','19','20','21','22','23','24'],
    y=['E','A','D','G','B','e']
    )
  ])
py.plot(data, filename="Led_Zeppelin_Heartbreaker")

            
          
        
        

  
