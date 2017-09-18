import json
import re

with open('pizza-train.json') as json_data:
    #initalize
    data = json.load(json_data)
    #--takes all words and numbers, but removes all words with _ in between
    regex = r'\b[^\W_|\w*_\w+]*\'?[^\W_]+\b'
    all_words = set()
    all_lines = []
    bag_of_words = [] # The big bag of words
    for d in data:
        # each request text is transfered to lower case letters and assign to the text variable
        text = d["request_text"].lower() 
        emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)',text)
        sentence = re.findall(regex,text) + emoticons #use both emoticons and the regex
        word_count = {} # a container for each distinctive word in the text
        
        # iterate through the words and add the words to the variable all_words so that all_words contains all the words
        # since it is a set, it will only contain each word once
        for word in sentence:
            all_words.add(word.encode('ascii','ignore')) #tranlate from uniicode generated from the regex
            if word not in word_count:
                word_count[word] = 1
            else:
                word_count[word] += 1
        all_lines.append(word_count)
        
    # loop through all the dictonaries and add the word counts for each sentance to the 
    # matrix varible which is the big bag of words
    for line in all_lines:
        bag_of_words_inner = []
        for word in all_words:
            if word in line:
                bag_of_words_inner.append(line[word])
            else:
                bag_of_words_inner.append(0)
        bag_of_words.append(bag_of_words_inner)
   
    print all_words
    print       
    print bag_of_words