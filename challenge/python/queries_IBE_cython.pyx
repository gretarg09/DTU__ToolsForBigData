import time


def getPattern(pattern):
    '''
    purpose: get the pattern to a form which is nice to work with
    input: string on the from "a[num, num]b[num, num]c..."
    output: list on the form ["a", [num,num], "b", [num, num], "c",...]
    '''
    pattern = pattern.replace('[', ']') # know all the parts of the pattern are seperated by ]
    pattern = pattern.split(']')
    pattern_sequence = []
    for i in range(len(pattern)):
        # if i is even we know that we have the numbers so we split them on , and append to
        # a list
        if i % 2:
            nums = pattern[i].split(',')
            nums = [int(num) for num in nums]
            pattern_sequence.append(nums)

        else:
            pattern_sequence.append(pattern[i])
    return pattern_sequence


def main(pattern_string):
    pattern = getPattern(pattern_string)
    print pattern

    #fileUri = "/Users/GretarAtli/Dropbox/Dtu/Tools_For_Big_Data/Exercises/challenge_1/wiki_english_art_cat_preproc.xml"
    fileUri = "/Users/GretarAtli/Dropbox/Dtu/Tools_For_Big_Data/Exercises/challenge_1/a_preproc.xml"
    fileUri_answer = "/Users/GretarAtli/Dropbox/Dtu/Tools_For_Big_Data/Exercises/challenge_1/answers/"
    fileUri_answer = fileUri_answer + "a_" + pattern_string + ".txt"

    # Initalize counters and results
    #t0 = time.time()

    #results = [word[2] for word in results]
    # write the solution in a nice way
    w = open(fileUri_answer, 'w')

    t0 = time.time()
    cdef int start_index = 0 # so we can loop thorugh all the first letters in the pattern
    cdef int key_counter = 0
    cdef int all_first_pattern = 0
    cdef int end_index = 0
    cdef str text_under_inspection = ""
    cdef int match_sum = 0
    cdef int result_sum = 0
    cdef str string_container = ""

    with open(fileUri) as f:
        for line in f:
            test_string = line  
            #print line
            results = {}

            start_index = 0 # so we can loop thorugh all the first letters in the pattern
            key_counter = 0
            all_first_pattern = 0
            end_index = 0
            text_under_inspection = ""

            all_first_pattern = test_string.count(pattern[0])
            # loop through all all cases of the first string pattern
            for i in range(all_first_pattern):
                start_index = test_string.index(pattern[0], start_index) + len(pattern[0])
                text_under_inspection = ''
                end_index = min(len(test_string), start_index + pattern[1][1] + len(pattern[2]))
                for j in range(start_index, end_index):
                    text_under_inspection += test_string[j]
                    if text_under_inspection[-len(pattern[2]):] == pattern[2] and len(text_under_inspection) > pattern[1][0]:
                        results[key_counter] = (start_index, start_index + len(text_under_inspection), pattern[0] + text_under_inspection)
                        key_counter += 1
                start_index += 1 - len(pattern[0])
            # If we have more than one pattern, we go to this loops and finish the query
            # The idea is that since we have now matched the first 3 parts of the string, we can now
            # loop by jumpying two steps and check ahead if there are x-many characters in the next string
            # The reason why we loop on 2 is that we know that in total the pattern must be odd, because it starts
            # and ends with a string, but we have matched the odd above so we now this loop will be even
            if len(pattern) > 3:
                temp_pattern = pattern[3:]
                # the ideal is to just a method infuenced from dynamic programming,
                for i in range(1, len(temp_pattern), 2):
                    for key, value in results.items():
                        old_start_index, start_index, sub_result = value
                        text_under_inspection = ''
                        end_index = min(start_index + temp_pattern[i - 1][1] + len(temp_pattern[i]), len(test_string))

                        for j in range(start_index, end_index):
                            text_under_inspection += test_string[j]
                            if text_under_inspection[-len(temp_pattern[i]):] == temp_pattern[i] \
                                    and len(text_under_inspection) > temp_pattern[i - 1][0]:
                                results[key_counter] = \
                                    (old_start_index, start_index + len(text_under_inspection),sub_result + text_under_inspection)
                                key_counter += 1
                        del results[key]
            results = set(results.values())

            match_sum = match_sum + len(results)
            if len(results) > 0:
                result_sum = result_sum + 1
                #string_container = string_container +  "matches: {}".format(str(len(results)))
                for match in results:
                    #w.write("\n")
                    #w.write(match[2])
                    string_container = string_container + "\n" + match[2]
                    #string_container = string_container + "\n" + str(match[0]) + "-" + str(match[1]) + "_: " + match[2]

                #w.write("\n")
        t1 = time.time()

        w.write("\n---------- statistics ----------\n")
        w.write("Got {} results and {} matches \n".format(result_sum, match_sum))
        w.write("The total execution time was {} sec \n".format(t1 - t0))
        w.write("\n")
        w.write("Resulting matching strings:\n")
        w.write(string_container)

    w.close()

#main('or[0,10]or[0,10]or')
#main('elephants[0,20]are[0,20]to')
#main('big[0,20]data[0,20]query')
#main('hopefully[10,20]no[10,20]matches')