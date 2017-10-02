import json
import re
import time

def getPattern(pattern):
    pattern_split = pattern.replace('[',']')
    pattern_split = pattern_split.split(']')
    
    pattern_container = {
        "keys" : [],
        "restrictions" : [],
        "index" : []
    }
    
    for i,p in enumerate(pattern_split):
        if i%2 == 0:
            pattern_container["keys"].append(p.lower())
        if i%2 == 1:
            nr1,nr2 = p.split(",")
            pattern_container["restrictions"].append([int(nr1),int(nr2)])
    # add the last element onto the patterna container list
    return pattern_container

def validate(matches,current_pos,level):
    print level
    indexes = [i for i in pattern_container["index"][level] if i > current_pos]
    restrictions = pattern_container["restrictions"][level-1]
    
    for i in indexes:
        previous_word = pattern_container["keys"][level-1]
        if restrictions[0] <=  i -  (len(previous_word) + current_pos)  <= restrictions[1]:
            incremented_matches = matches + [i]
            if level  == len(pattern_container["keys"]) - 1:
                start_index = incremented_matches[0]
                end_index = incremented_matches[-1] + len(pattern_container["keys"][-1])
                # print incremented_matches
                result.add(query[start_index:end_index])
            elif level < len(pattern_container["keys"]) - 1:
                validate(incremented_matches,i,level+1)
        else: break


#incoming = "ammmbnnnbncnnc"
#pattern = "A[0,20]B[0,20]C[0,20]"

#incoming = "aammbnnnbncnnc"
#pattern = "A[0,20]B"

incoming = "I have a really nice cat in hat at home"
pattern = "have[0,20]cat[2,7]hat[0,20]home"

#incoming = 'I have a really nice cat in hat at home'
#pattern = 'cat[2,4]hat'

#fileUri = "/Users/GretarAtli/Dropbox/Dtu/Tools_For_Big_Data/Exercises/challenge_1/wiki_english_art_cat_preproc.xml"
#fileUri = "/Users/GretarAtli/Dropbox/Dtu/Tools_For_Big_Data/Exercises/challenge_1/wiki_english_art_cat_preproc.xml"

incoming 
#pattern = 'cats[0,10]are[0,10]to'
#pattern = 'or[0,10]or[0,10]or'
#pattern = 'when[15,25]republic[15,25]along'

# initialize global parameters        
global query # the string that is being queried
global pattern_container # a pattern container
global result # container for the matchin strings

query = incoming
pattern_container = getPattern(pattern)
result = set()

#print "The query is {}".format(query)
print "The keys are {} \n".format(pattern_container["keys"])

indexes = []
for key in pattern_container["keys"]:
    indexes.append([m.start() for m in re.finditer('(?={})'.format(key), query)])

pattern_container["index"] = indexes

#print "\n container \n"
#print pattern_container    

#print "start \n"

# going through the first list
for i in pattern_container["index"][0]:
    validate([i],i,1)

print "The result is : \n"
if result:
    for i in result:
        print i
else:
    print "no match in this text"

# delete from memory
del result
del incoming      

        # delete from memory
        del result
        del incoming