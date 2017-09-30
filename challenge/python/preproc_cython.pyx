import json
import re

def __main__(): 
    #fileUri = "/Users/GretarAtli/Dropbox/Dtu/Tools_For_Big_Data/Exercises/challenge_1/wiki_english_art.xml"
    #processedFileUri = "/Users/GretarAtli/Dropbox/Dtu/Tools_For_Big_Data/Exercises/challenge_1/wiki_english_art_preprocessed.xml"

    cdef str fileUri = "/Users/GretarAtli/Documents/GitHub/Dtu/Dtu-ToolsForBigData/challenge/mini.xml"
    cdef str processedFileUri = "/Users/GretarAtli/Documents/GitHub/Dtu/Dtu-ToolsForBigData/challenge/mini_processed.xml"

    cdef int position = 0
    cdef str regex = ""
    cdef str text = ""

    # position 0 means that the program is currently reading lines that are not between <text><\text>
    # position 1 means that the program is currently reading lines that are between <text><\text>

    # open a file to write in 
    w = open(processedFileUri, 'w')

    with open(fileUri) as f:
        for line in f:
            #  convert line breaks to spaces. Convert all upper case letters to lower case letters. 
            line = line.replace("\n","").lower()

            if position == 0 :
                reresult = re.findall("<text.*>(.*)",line)
                if reresult:
                    text = text + reresult[0]
                    position = 1
            elif position == 1:
                reresult = re.findall("(.*)</text>", line)
                if reresult:
                    text = text + reresult[0]
                    position = 0
                    # write to file
                    w.write(text)
                    # initialize the string as a empty string
                    text = ""
                else:
                    text = text + line
    w.close()