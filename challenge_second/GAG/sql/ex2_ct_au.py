import sqlite3
from datetime import datetime

DB_PATH = "/Users/GretarAtli/Documents/GitHub/Dtu/Dtu-ToolsForBigData/challenge_second/GAG/reddit.db"

t0 = datetime.now()

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
query = '''
    	SELECT subreddit_id ,count(distinct author_id)
        FROM comments
        Group BY subreddit_id
'''


cursor.execute(query)
data =  cursor.fetchall()
t1 = datetime.now()
print(data)
print(t1-t0)

list_sorted =sorted(data, key=lambda x: x[1],reverse=True)

counter = 0
#print('{:<2} & {:<25} & {:<15} & {:<15}'.format('##','Subreddit','Average Depth','Time'))
for i in list_sorted:
	counter = counter + 1
	q = '''
		SELECT name
			FROM subreddits
			WHERE id = ?
	'''

	cursor.execute(q,[i[0]])
	data = cursor.fetchall()

	print('{}.  {:<25}  {:<15.2f} '.format(counter,data[0][0],i[1]))
	if counter > 9:
		break
