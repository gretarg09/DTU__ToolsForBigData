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
    #print level
    indexes = [i for i in pattern_container["index"][level] if i > current_pos]
    restrictions = pattern_container["restrictions"][level-1]
    
    #t3 =  time.time()
    
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
    
    #t4 = time.time()
    #print t4-t3
 
def main(pattern):           
    #pattern = 'cats[0,10]are[0,10]to'
    #pattern = 'or[0,10]or[0,10]or'
    #pattern = 'when[15,25]republic[15,25]along'

    fileUri = "/Users/GretarAtli/Dropbox/Dtu/Tools_For_Big_Data/Exercises/challenge_1/wiki_english_art_cat_preproc.xml"
    #fileUri = "/Users/GretarAtli/Dropbox/Dtu/Tools_For_Big_Data/Exercises/challenge_1/wiki_english_art_cat_preproc_double.xml"
    #fileUri = "/Users/GretarAtli/Dropbox/Dtu/Tools_For_Big_Data/Exercises/challenge_1/wiki_english_art_a_preproc.xml"

    # initialize global parameters        
    global query # the string that is being queried
    global pattern_container # a pattern container
    global result # container for the matchin strings

    t0 = time.time()
    counter = 1

    # open a file to process the data
    with open(fileUri) as f:
        for line in f:
            incoming = line
            query = incoming
            
            pattern_container = getPattern(pattern)
            result = set()

            #print "The query is {}".format(query)
            #print "The keys are {} \n".format(pattern_container["keys"])

            #t3 = time.time()
            
            indexes = []
            for key in pattern_container["keys"]:
                indexes.append([m.start() for m in re.finditer('(?={})'.format(key), query)])

            pattern_container["index"] = indexes

            #t4 = time.time()
            #print "index time {}".format(t4-t3)
            
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

            print counter
            counter = counter + 1
            
            # delete from memory
            del result
            del incoming

    t1 = time.time()
    print "\nthe execution time was {}".format(t1-t0)

main('or[0,10]or[0,10]or')
