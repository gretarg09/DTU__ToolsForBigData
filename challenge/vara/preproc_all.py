import json
import re
import time

fileUri = "/Users/GretarAtli/Dropbox/Dtu/Tools_For_Big_Data/Exercises/challenge_1/wiki_english_art.xml"
processedFileUri = "/Users/GretarAtli/Dropbox/Dtu/Tools_For_Big_Data/Exercises/challenge_1/wiki_english_art_preproc.xml"

#fileUri = "/Users/GretarAtli/Documents/GitHub/Dtu/Dtu-ToolsForBigData/challenge/mini.xml"
#processedFileUri = "/Users/GretarAtli/Documents/GitHub/Dtu/Dtu-ToolsForBigData/challenge/mini_processed.xml"

position = 0 # The state of the program. More info down below
counter = 0 # counts the number of article that have been processed
text = "" # a container for the text

with open(fileUri) as f:
    for line in f:
        #  convert line breaks to spaces. Convert all upper case letters to lower case letters. 
        line = line.replace("\n"," ").lower()
        if position == 0 :
            reresult = re.findall("<text.*>(.*)",line)
            # if the string contains the substring <text then we need to start collection the words
            if reresult:
                #check if the string contains <\text> to handle the case of <text> and </text> in the same line
                reTextEndingResult = re.findall("<text.*>(.*)</text>", line)
                if reTextEndingResult:
                    counter += 1
                    # writing the last part of the page and adding a linebreak in the end
                    text = text + reTextEndingResult[0] + "\n"
                    position = 0
                    w.write(text)
                    text = "" # initialize the string as a empty string
                else:
                    text = text + reresult[0]
                    position = 1
        elif position == 1:
            reTextEndingResult = re.findall("</text>", line)
            if reTextEndingResult:
                reTextEndingResult = re.findall("(.*)</text>", line)
                counter += 1
                if counter % 1000 == 0:
                    print counter
                # writing the last part of the page and adding a linebreak in the end
                text = text + reTextEndingResult[0] + "\n"
                position = 0
                w.write(text) # initialize the string as a empty string
                text = ""
            else:
                text = text + line
w.close()

t1 = time.time()

print (t1-t0)