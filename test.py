#! /usr/bin/env python

previous_freqs = { 60:0, 61:0, 62:0, 63:0, 64:0, 65:0, 66:0, 67:0, 68:0, 69:0, 70:0, 71:0 }
current_freqs = { 60:0, 61:0, 62:0, 63:0, 64:0, 65:0, 66:0, 67:0, 68:0, 69:0, 70:0, 71:0 }

current_frame = [0,1,2]

if int(2) in current_frame:
	print "ja"
current_freqs[60] = 1000
print current_freqs