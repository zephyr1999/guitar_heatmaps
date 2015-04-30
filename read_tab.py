# program to split up guitar tab into string and fret information
# note that with this program, i'm just getting individual note information,
# note note order or phrasing or any of that nonsense.

import numpy
import plotly.plotly as py
from plotly.graph_objs import *


filename = "lz_01.txt"

# first, get a list of each line
with open(filename) as f:
    tab = f.readlines()

#string data will hold all of the string fret info
string_data = [[],[],[],[],[],[]]
#string 0 is high E, 1 is B, 2 is G, 3 is D, 4 is A, and 5 is low E

# go through each line and check if it begins with a string character,
# which is usually |

i = 0

while i < len(tab):

	if tab[i][0] == "|":
		# this means this is the high E string
		# so go through 6 lines of strings before checking again
		for j in range(0,6):
			# use i+j to go through all 6 strings
			k = 0
			while (k < len(tab[i+j])):
				# check if each character is a number
				if tab[i+j][k].isdigit():
					#first check if next number is also digit (i.e. 2 followed by 4)
					# 	should be stored as '24' and not '2','4'
					if tab[i+j][k+1].isdigit():
						#increment the correct string count
						
						# TODO: for some reason this is just skipping the second digit
						# ''.join connects the two characters
						# print (tab[i+j][k] + tab[i+j][k+1])
						string_data[j].append(int(''.join(tab[i+j][k] + tab[i+j][k+1])))
						# increment k to skip over next char
						k = k + 1
					else:
						string_data[j].append(int(tab[i+j][k]))
						
				# increment k to next char		
				k = k + 1
						
		#increment i to skip over next 5 lines					
		i = i + 5
	
	#now do the same but with -
	elif tab[i][0] == "-":
		# this means this is the high E string
		# so go through 6 lines of strings before checking again
		for j in range(0,6):
			# use i+j to go through all 6 strings
			k = 0
			while (k < len(tab[i+j])):
				# check if each character is a number
				if tab[i+j][k].isdigit():
					#first check if next number is also digit (i.e. 2 followed by 4)
					# 	should be stored as '24' and not '2','4'
					if tab[i+j][k+1].isdigit():
						#increment the correct string count
						
						# TODO: for some reason this is just skipping the second digit
						# ''.join connects the two characters
						# print (tab[i+j][k] + tab[i+j][k+1])
						string_data[j].append(int(''.join(tab[i+j][k] + tab[i+j][k+1])))
						# increment k to skip over next char
						k = k + 1
					else:
						string_data[j].append(int(tab[i+j][k]))
						
				# increment k to next char		
				k = k + 1
						
		#increment i to skip over next 5 lines					
		i = i + 5
		
	#increment i to next line
	i = i + 1
	
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

						
					
				
				

	
