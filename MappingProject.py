# PASSED OFF ROSALIND PROBLEM IN 35 SECONDS (9,500 char reference genome and 15,000 reads)
import sys
from parser import grabReads, grabGenome
globalstr = {} #globalstr["text"] holds the seq
suffixArray = [];
first = []; # seq at suffix array. chars in order of s array
BWT = []; # Use the suffix array. chars in order of s array -1
ltf = []; # look in first to find the indices where chars in BWT occur
text = "";
patterns = [];

def readFile():
	counter = 0;
	with open( sys.argv[1] ) as fh:
		for line in fh:
			if counter > 0:
				patterns.append(line[0:len(line)-1].upper());
			else:
				globalstr["text"] = (line[0:len(line)-1]+"$").upper();
				text = str(line[0:len(line)-1]).upper();
			counter += 1;
	return patterns;

def getRange(indices,first,char,obj):

	obj["foundFirst"] = False;
	obj["foundLast"] = False;
	for i in range(len(indices)):
		element = first[indices[i]];
		#print("ELEMENT: " + element);
		c, num = element.split('_', 1);
		if char == c and not obj["foundFirst"]:
			obj["firstIndex"] = indices[i];
			obj["foundFirst"] = True;
		if char != c and obj["foundFirst"]:
			obj["lastIndex"] = indices[i-1];
			obj["foundLast"] = True;
			break;
	if obj["foundFirst"] and not obj["foundLast"]:
		obj["foundLast"] = True;
		obj["lastIndex"] = indices[-1];

	return obj;


def findOccurances(patterns,first,BWT,ltf):
	results = [];
	counter = 0;
	#print(first);
	#print(BWT);
	#print(ltf);
	obj = {}
	counterStr = 0;
	for string in patterns: # FOR EACH PATTERN
		counterStr += 1;
		if counterStr % 100 == 0:
			print(counterStr);
		#print(string);
		lastChar = string[-1];
		firstIndex = 0;
		lastIndex = 0;
		if lastChar == "A" or lastChar == "a":
			firstIndex = FirstCharOccurances[0];
			lastIndex = FirstCharOccurances[1];
		if lastChar == "C" or lastChar == "c":
			firstIndex = FirstCharOccurances[1];
			lastIndex = FirstCharOccurances[2];
		if lastChar == "G" or lastChar == "g":
			firstIndex = FirstCharOccurances[2];
			lastIndex = FirstCharOccurances[3];
		if lastChar == "T" or lastChar == "t":
			firstIndex = FirstCharOccurances[3];
			lastIndex = len(first);
		#indices = range(0,len(first));
		indices = range(firstIndex,lastIndex);	#This cuts the time in half by narrowing down the indices to compare to the first char in the reversed string
		counter += 1;
		#print(counter);
		#print("pattern: " + str(string));
		for iterator1 in range(len(string)): #FOR EACH CHAR BACKWARDS IN PATTERN
			reverseString = string[::-1];
			c = reverseString[iterator1];
			#print("character: " + c);
			positionRange = getRange(indices,first,c,obj); #FIND
			#print("range: " + str(positionRange));
			if not positionRange["foundFirst"]:
				break;

			if iterator1 == len(string)-1:
				for i in range(positionRange["firstIndex"],positionRange["lastIndex"]+1):
					results.append(suffixArray[i]);
			else:
				nextChar = reverseString[iterator1+1];
				indices = [];
				for i in range(positionRange["firstIndex"],positionRange["lastIndex"]+1):
					#print(i);
					if nextChar == BWT[i][0]:
						#print(ltf[i]);
						indices.append(ltf[i]);
	results.sort();
	return results;

def getIndex(suffix, text):
	return text.find(suffix);

def createSuffixes(text):
	suffixes = [];
	for i in range(0,len(text)):
		suffixes.append(text[i:len(text)]);
	return suffixes;

def getSuffixArray(text):
	suffixes = createSuffixes(text);
	suffixes.sort();

	indices = [];
	for suffix in suffixes:
		index = getIndex(suffix,text);
		indices.append(index);

	return indices;

def printStringIndices(result):
	strin = "";
	for index in result:
		strin += str(index) + " ";

	return strin;

def getFirst(suffixArray, FirstCharOccurances):
	first = [];
	counter = 0;
	Acounter = 0;
	Ccounter = 0;
	Gcounter = 0;
	Tcounter = 0;
	currentChar = globalstr["text"][suffixArray[0]];
	for index in suffixArray:
		char = globalstr["text"][index];
		if char == "A" or char == "a":
			char = "A";
			Acounter += 1;
			counter = Acounter;
			if Acounter == 1:
				FirstCharOccurances.append(len(first));	#This FirstCharOccurances shenanigans is an optimization for searching that cuts the time in half
		elif char == "C" or char == "c":
			char = "C";
			Ccounter += 1;
			counter = Ccounter;
			if Ccounter == 1:
				FirstCharOccurances.append(len(first));
		elif char == "G" or char == "g":
			char = "G";
			Gcounter += 1;
			counter = Gcounter;
			if Gcounter == 1:
				FirstCharOccurances.append(len(first));
		elif char == "T" or char == "t":
			char = "T";
			Tcounter += 1;
			counter = Tcounter;
			if Tcounter == 1:
				FirstCharOccurances.append(len(first));
		else:
			counter = 1;
		first.append(char+"_"+str(counter));
	#print(FirstCharOccurances);
	return first;

def getBWT(suffixArray):
	BWT = [];
	counter = 0;
	Acounter = 0;
	Ccounter = 0;
	Gcounter = 0;
	Tcounter = 0;
	currentChar = globalstr["text"][suffixArray[-1]];
	for index in suffixArray:
		char = globalstr["text"][index-1];
		if char == "A" or char == "a":
			char = "A";
			Acounter += 1;
			counter = Acounter;
		elif char == "C" or char == "c":
			char = "C";
			Ccounter += 1;
			counter = Ccounter;
		elif char == "G" or char == "g":
			char = "G";
			Gcounter += 1;
			counter = Gcounter;
		elif char == "T" or char == "t":
			char = "T";
			Tcounter += 1;
			counter = Tcounter;
		else:
			counter = 1;
		BWT.append(char+"_"+str(counter));

	return BWT;


def getLTF(first,BWT):
	LTF = [];
	for element in BWT:
		index = first.index(element);
		LTF.append(index);
	return LTF;

def printSAM(results):
	out = "";
	length = len(patterns[0]);
	counterLine = 0;
	for i in range(len(results)):
		counterLine += 1;
		if counterLine % 10000 == 0:
			print(counterLine);
		piece = globalstr["text"][results[i]:results[i]+length];
		out += "R" + str(i+1) + "\t" + "0" + "\t" + "Chr1" + "\t" + str(results[i]+1) + "\t" + "255" + "\t" + str(length) + "M" + "\t" + "*" + "\t" + "0" + "\t" + "0" + "\t" + piece + "\t" + "*" + "\n";

	return out;

FirstCharOccurances = []; # This will help us know where the first of each char A C G and T occur in the First Array


print("reading file...");
patterns = readFile();
print("done reading file");
print("creating Suffix Array...");
suffixArray = getSuffixArray(str(globalstr["text"]));
print("done creating Suffix Array");
print("getting first array...");
first = getFirst(suffixArray,FirstCharOccurances);
print("done creating first array");
print("creating BWT...");
BWT = getBWT(suffixArray);
print("done creating BWT");
print("creating Last to First...");
ltf = getLTF(first,BWT);
print("done creating last to first");
#print(first);
#print(BWT);
#print(ltf);
print("finding occurrences...");
results = findOccurances(patterns,first,BWT,ltf);
print("done finding occurrences");
print("printing results...");
toPrint = printStringIndices(results);
print("done creating indices");
#print(toPrint);
toPrintSAM = printSAM(results);
#print(toPrintSAM);
print("Done creating SAM list");
print("Writing SAM file...");
f = open('out.txt','w')
f.write(toPrint) # python will convert \n to os.linesep
f.close()

f = open('out.sam','w')
f.write(toPrintSAM) # python will convert \n to os.linesep
f.close()
print("ALL DONE");
