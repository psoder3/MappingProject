#! usr/bin/env python

import re
import sys

def grabGenome(fh):
	return "".join( [line.strip() for line in fh if line[0] != '>' ] )

def grabReads(fh):
	return re.findall('^[AGTCagtc]+$', fh.read(), re.M)

if __name__ == "__main__":
	genome = ""
	reads = []
	with open(sys.argv[1], 'r') as fhGenome:
		genome = grabGenome(fhGenome)
	with open(sys.argv[2], 'r') as fhReads:
#		if sys.argv[3] == 'fasta':
#			reads = fasta( fhReads.read())
#		if sys.argv[3] == 'fastq':
		reads = grabReads( fhReads)
	with open(sys.argv[3], 'w') as outfile:
		outfile.write( genome )
		outfile.write( '\n'   )
		for read in reads:
			outfile.write( read )
			outfile.write( '\n'  )
