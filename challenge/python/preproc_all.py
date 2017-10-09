import json
import re
import time

fileUri = "/Users/GretarAtli/Dropbox/Dtu/Tools_For_Big_Data/Exercises/challenge_1/enwiki-20170820-pages-articles-multistream.xml"
processedFileUri = "/Users/GretarAtli/Dropbox/Dtu/Tools_For_Big_Data/Exercises/challenge_1/all_preproc.xml"

#fileUri = "/Users/GretarAtli/Dropbox/Dtu/Tools_For_Big_Data/Exercises/challenge_1/mini_tail.xml"
#processedFileUri = "/Users/GretarAtli/Dropbox/Dtu/Tools_For_Big_Data/Exercises/challenge_1/mini_tail_a_p_2.xml"


position = 0 # The state of the program. More info down below
counter = 0 # counts the number of article that have been processed
isRedirect = False
text = "" # a container for the text

t0 = time.time()

# position 0 means that the program is currently reading lines that are not between <text><\text>
# position 1 means that the program is currently reading lines that are between <text><\text>

# open a file to write in 
w = open(processedFileUri, 'w')

with open(fileUri) as f:
    for line in f:    
        #  convert line breaks to spaces. Convert all upper case letters to lower case letters. 
        #line = line.replace("\n"," ").lower()
        #line = line.replace(" +"," ")
        #line = re.sub(r"\n+"," ",line).lower()
        #line = re.sub(r'[\n\r]+', r' ', line)
        
        if position == 0 : 
            # Try to find a redirect tag
            if(re.match(".*<redirect(.*)/>",line)):
                isRedirect = True
                
            # Next we find the namespace of the page
            re_namespace = re.findall("<ns>(.*)</ns>",line)
            if re_namespace:
                namespace = int(re_namespace[0])
                #print namespace
            
            # If the string contains the substring <text then we need to start collecting the words
            reresult = re.findall("<text.*>(.*)",line)
            if reresult:
                
                # Now we need to check wheater the text starts with #redirect
                if re.match("^#redirect",reresult[0]):
                    isRedirect = True
                
                # Check if the string contains <\text> to handle the case of <text> and </text> in the same line
                reTextEndingResult = re.findall("<text.*>(.*)</text>", line)
                
                if reTextEndingResult:
                    counter += 1
                    # Writing the last part of the page and adding a linebreak in the end
                    text = text + reTextEndingResult[0]
                    position = 0
                    # If it is not a redirect page then we write the string to a file
                    if isRedirect == False and namespace == 0:
                        text = re.sub(r"\n+"," ",text).lower()
                        text = text + "\n"
                        w.write(text)
                    isRedirect = False # Initialize the redirect boolean variable
                    namespace = -1 # Initialize the namespace as -1
                    text = "" # Initialize the string as a empty string
                else:
                    text = text + reresult[0]
                    position = 1
        elif position == 1:
            # check if the string contains <\text> tag, if so we write the collected text to a file
            reTextEndingResult = re.findall("</text>", line)
            if reTextEndingResult:
                reTextEndingResult = re.findall("(.*)</text>", line)
                counter += 1
                if counter % 1000 == 0:
                    print counter
                # Writing the last part of the page and adding a linebreak in the end
                text = text + reTextEndingResult[0]
                position = 0
                # If it is not a redirect page then we write the string to a file
                if isRedirect == False and namespace == 0:
                    text = re.sub(r"\n+"," ",text).lower()
                    text = text + "\n"
                    w.write(text)
                isRedirect = False # Initialize the redirect boolean variable
                namespace = -1 # Initialize the namespace as -1
                text = "" # Initialize the string as a empty string
            else:
                text = text + line 
w.close()

t1 = time.time()

print (t1-t0)