import os
from multiprocessing import Process
import sqlite3
from datetime import datetime
from multiprocessing import Pool
import string

# Connect to the database
conn = sqlite3.connect("reddit.db")
# For encoding purpose.
#conn.text_factory = lambda x: str(x, 'latin1')
#Cursor to the Northwind database
conn.text_factory = str
cursor = conn.cursor()

def querying(Subreddit):
    start_time = datetime.now()
    # #print the result.
    print Subreddit
    query =  """
                SELECT Distinct body
                From Comments      
                Where subreddit_id = ?
            """
    cursor.execute(query,Subreddit)
    start_timeAfterDB = datetime.now()    

    print 'Query Time: {}'.format(start_timeAfterDB - start_time)
    #wordSet = set()
    #translator = string.maketrans("","")
    translator = (string.maketrans('', ''), string.punctuation)
    wordSet = set()
    #maper = str.maketrans('', '', 'aeiouAEIOU')
    #print 'Loop through comments'
    #theComments = []
    #theWord = []
    data = cursor.fetchall()
    for comment in data:
        comment = comment[0]
        comment = comment.lower()
        comment = comment.translate(string.maketrans("",""), string.punctuation)
        wordSet.update(tuple(word for word in set(comment.split()) if word))


    end_time = datetime.now()
    elapsed_time = end_time - start_time
    elapsed_time_DB = end_time - start_timeAfterDB
    sizeofSet = len((wordSet))
    print 'The Subreddit: {} and the nr of unq words: {} and the time: {}'.format(Subreddit[0],sizeofSet,elapsed_time)
    print 'Just looping through comment time {}'.format(elapsed_time_DB)
    return Subreddit[0],sizeofSet
          


 
if __name__ == '__main__':


    query2 = """
            SELECT distinct(subreddit_id)
            From Comments      
            --where subreddit_id = 't5_21nj'
            --order by subreddit_id desc
            Limit 100
        """
    cursor.execute(query2)
    #t5_2qh0s t5_2fwo t5_2qh0u
    #print 'Hello, this?'.translate(string.maketrans("",""), string.punctuation)
    multiPr = 1
    Allstart_time = datetime.now()
    if multiPr:
        p = Pool(8)
        results = p.map(querying, cursor.fetchall())
        #print results
        p.close()
        p.join()
    else:
        #print('Call functions')
        for i in cursor.fetchall():
            results = querying(i)
            print results
    conn.close()
    print results
    Allend_time = datetime.now()
    elapsed_time = Allend_time - Allstart_time
    print 'Total Time: {0}'.format(elapsed_time)