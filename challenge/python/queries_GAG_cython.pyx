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

cpdef validate(int pos_first_match, int current_pos, int level, int stop_level):
    #print level
    curr_indexes = [i for i in indexes[level] if i > current_pos]

    for i in curr_indexes:
        previous_word = keys[level-1]
        if restrictions[level-1][0] <=  i - (len(previous_word) + current_pos)  <= restrictions[level-1][1]:
            if level  == stop_level:
                result.add(query[pos_first_match: i + len(keys[-1])])
            elif level < len(keys) - 1:
                validate(pos_first_match,i,level+1,stop_level)
        else: break
    
    #t4 = time.time()
    #print t4-t3
def main(p):
    #pattern = 'cats[0,10]are[0,10]to'
    pattern = p
    #pattern = 'when[15,25]republic[15,25]along'

    #fileUri = "/Users/GretarAtli/Dropbox/Dtu/Tools_For_Big_Data/Exercises/challenge_1/wiki_english_art_cat_preproc.xml"
    #fileUri = "/Users/GretarAtli/Dropbox/Dtu/Tools_For_Big_Data/Exercises/challenge_1/wiki_english_art_cat_preproc_double.xml"
    fileUri = "/Users/GretarAtli/Dropbox/Dtu/Tools_For_Big_Data/Exercises/challenge_1/wiki_english_art_preproc.xml"

    #counter = 1

    # initialize global parameters        
    global query # the string that is being queried
    global indexes # a pattern container
    global keys # list of keys
    global restrictions #list of restrictions
    global result # container for the matchin strings
    
    pattern_container = getPattern(pattern)

    indexes = []
    keys  = pattern_container["keys"]
    restrictions = pattern_container["restrictions"]
    
    #t0 = time.time()
    #i = 0

    # open a file to processs the data
    with open(fileUri) as f:
        for line in f:
            
            query = line
            result = set()
            
            for key in pattern_container["keys"]:
                indexes.append([m.start() for m in re.finditer('(?={})'.format(key), query)])

            # going through the first list      
            for i in indexes[0]:
                validate(i,i,1,len(pattern_container["keys"])-1)

            #print "The result is : \n"
            #if result:
            #    for i in result:
            #        print i
            #else:
            #    print "no match in this text"

            #print counter
            #counter = counter + 1

            # delete from memory
            del result

    #t1 = time.time()
    #print "\nthe execution time was {}".format(t1-t0)

#main('or[0,10]or[0,10]or')