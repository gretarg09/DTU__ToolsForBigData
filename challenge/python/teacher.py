def get_matches_starting_at(data, pattern, index, starting_index, resulting_matches):
	sub_data = data[index:]

	P = pattern[0]
	if sub_data[:len(P)] == P:
		if len(pattern) == 1:
			resulting_matches.append((starting_index,index+len(P)))
		else:
			for new_index in range(pattern[1][0]+1, pattern[1][1]+2):
				get_matches_starting_at(data, pattern[2:], index+len(P)+new_index-1, starting_index, resulting_matches)
		
		return resulting_matches
	else:
		return []

def get_all_matches(data, pattern):
	matches_found = []
	for index in range(len(data)):
		matches_at_index = get_matches_starting_at(data, pattern, index, index, [])
		matches_found += matches_at_index
		
	return set(matches_found)


#data = "testcatinhatinhatinhatinhat"
#pattern = ["cat",(2,12),"hat"]
fileUri = "/Users/GretarAtli/Dropbox/Dtu/Tools_For_Big_Data/Exercises/challenge_1/a_preproc.xml"
pattern = ['arnold',[0,10],'schwarzenegger',[0,10],'is']
#pattern = ["A",(6,7),"CC",(2,6),"GT"]

with open(fileUri) as f:
	for line in f:
		data = line
		matches = get_all_matches(data,pattern)

		#print "Results"
		for m in matches:
			print m, data[m[0]:m[1]]