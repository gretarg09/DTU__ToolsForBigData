#% Get all the unique subreddit_ids
#The data is also dumped in a file
#Data is used from the list
cursor = conn.execute('SELECT subreddit_id, COUNT(subreddit_id)  FROM comments GROUP BY subreddit_id;')
list_subreddit=[line for line in cursor]
list_subreddit.sort(key=lambda x: x[1],reverse=True)

len_vocabulary_subredditid=[]
for i in range(len(list_subreddit)):
    #get the subreddit_id
    subreddit_id=str(list_subreddit[i][0])[1:]
    #query to get the body and save each body
    cursor = conn.execute(r"SELECT body FROM comments WHERE subreddit_id="+subreddit_id)
    each_subreddit=[line[0] for line in cursor]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
    #get the vocabulary 
    vocabulary_subredditid=set()
    for item in each_subreddit:
        vocabulary_subredditid.update(clean_subreddit(item.decode('utf-8')))
#        vocabulary_subredditid.update(clean_subreddit(str(item)[1:]))
    #save the final result
    len_vocabulary_subredditid.append([subreddit_id,len(vocabulary_subredditid)])