import time


def getPattern(pattern):
    pattern = pattern.replace('[',']')
    pattern=pattern.split(']')
    pattern_sequence = []
    for i in range(len(pattern)):
        if i % 2:
            nums = pattern[i].split(',')
            nums= [int(num) for num in nums]
            pattern_sequence.append(nums)
            
        else:
            pattern_sequence.append(pattern[i])
    return pattern_sequence


def main(pattern):

    with open("/Users/GretarAtli/Dropbox/Dtu/Tools_For_Big_Data/Exercises/challenge_1/wiki_english_art_cat_preproc.xml") as f:
        test_string = f.read()    
    pattern = getPattern(pattern)


    t0 = time.time()
    results = {}
    cdef int start_index = 0 # so we can loop thorugh all the first letters in the pattern
    cdef int key_counter = 0
    for i in xrange(test_string.count(pattern[0])):
        start_index = min(start_index, len(test_string)-1)
        start_index =test_string.index(pattern[0], start_index) + len(pattern[0]) 
        string = ''
        end_index = min(len(test_string),  start_index + pattern[1][1] + len(pattern[2])  + len(pattern[0]))
        for j in xrange(start_index , end_index): #her a ad verra pattern length i lykkjuni
            string += test_string[j]
            if string[-len(pattern[2]):] == pattern[2] and len(string) > pattern[1][0]:
                results[key_counter] = (start_index + len(string), pattern[0]+ string) #results[key_counter] = (start_index + len(string),  string) #  
                key_counter += 1

        start_index += 1
    t2 = time.time()
    if len(pattern) > 3:
        vec = pattern[3:]
        # the ideal is to just a method influenced from dynamic programming, 
        for i in xrange(1,len(vec), 2):
            for key, value in results.items():
                start_index, sub_result = value
                current_result = ''
                end_index = min(start_index + vec[i-1][1] + len(vec[i]), len(test_string))
                for j in range(start_index, end_index): 
                    current_result = ''.join([current_result, test_string[j]])
                    if current_result[-len(vec[i]):] == vec[i] and len(current_result) >vec[i-1][0]:
                        results[key_counter] = (start_index + len(current_result), sub_result + current_result)
                        key_counter += 1
                del results[key]
    
    print "The result is : \n"
    if results:
        for key,value in results.items():
            print value
    else:
        print "no match in this text"

        
    t1 = time.time()

    print "time", t1-t0
    print "time", t2-t0
    print t1 - t2

main('or[0,10]or[0,10]or')