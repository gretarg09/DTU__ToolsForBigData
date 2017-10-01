import json
import re
import time

fileUri = "/Users/GretarAtli/Dropbox/Dtu/Tools_For_Big_Data/Exercises/challenge_1/wiki_english_art.xml"
processedFileUri = "/Users/GretarAtli/Dropbox/Dtu/Tools_For_Big_Data/Exercises/challenge_1/wiki_english_art_cat_preproc.xml"

position = 0 # The state of the program. More info down below
counter = 0 # counts the number of article that have been processed
read = True # variable that controls if the article should be processed or not
text = "" # a container for the text
t0 = time.time()


# position 0 means that the program is currently reading lines that are not between <text><\text>
# position 1 means that the program is currently reading lines that are between <text><\text>

# open a file to write in 
w = open(processedFileUri, 'w')

with open(fileUri) as f:
    for line in f:
        #  convert line breaks to spaces. Convert all upper case letters to lower case letters. 
        line = line.replace("\n"," ").lower()
        
        # Check if title starts with A, if so then we 
        reresult = re.findall("<title>(.*)</title>",line)
        if reresult:
            # Stop reading when the articles do not start with a anymore
            if reresult[0] != ("cat"):
                read = False
            else:
                read = True
                print reresult[0]
        
        if read == True:
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
                        break
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
                    break
                else:
                    text = text + line
w.close()

t1 = time.time()

print (t1-t0)
        