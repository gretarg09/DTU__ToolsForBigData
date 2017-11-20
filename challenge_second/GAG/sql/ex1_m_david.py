import multiprocessing as mp
import sqlite3
import time
from collections import Counter

conn = sqlite3.connect('/Users/GretarAtli/Documents/GitHub/Dtu/Dtu-ToolsForBigData/challenge_second/GAG/reddit.db')

cursor = conn.cursor()
start_time = time.time()


def query_init():
    subreddits = []
    for row in cursor.execute("SELECT id FROM subreddits"):
        subreddits.append(row)
    return subreddits

def deepening(row):
    con = sqlite3.connect('/Users/GretarAtli/Documents/GitHub/Dtu/Dtu-ToolsForBigData/challenge_second/GAG/reddit.db')
    c = con.cursor()
    value = 0
    done = False
    while not done:
        items = c.execute("SELECT id, subreddit_id, parent_id FROM comments WHERE parent_id = ?", (row[0],)).fetchall()
        if not items:
            done = True
        for a in items:
            # deepening(a)
            row = a
            value += 1
    # print("DEPTH", value, row[1])
    return value, row[1]

def find_depth(chunks):
    top_ten = [("", 0)] * 10
    con = sqlite3.connect('/Users/GretarAtli/Documents/GitHub/Dtu/Dtu-ToolsForBigData/challenge_second/GAG/reddit.db')
    c = con.cursor()

    for i, subreddit in enumerate(chunks):
        values = [("", 0)]
        mean_value = c.execute("SELECT count(*) FROM comments WHERE parent_id  LIKE 't3%' AND subreddit_id = :subreddit", subreddit).fetchone()
        for row in c.execute("SELECT id, subreddit_id, parent_id FROM comments WHERE parent_id LIKE 't3%' AND subreddit_id = :subreddit", subreddit):
            value = deepening(row)
            # internalvalue += value[0]
            #
            curval = values[0][1] + value[0]
            if value[0] > values[0][1]:
                values[0] = (value[1],curval)
            else:
                values[0] = (values[0][0], curval)
        if mean_value[0]:
            values[0] = (values[0][0], values[0][1]/mean_value[0])
        else:
            values[0] = (values[0][0], values[0][1] / 1)
        if values[0] not in top_ten:
            depth = values[0][1]
            for i, item in enumerate(top_ten):
                if depth > item[1]:
                    top_ten[i] = values[0]
                    break

    print("Finished")
    print(top_ten)
    return top_ten


def chunk(list):
    chunks = int(float(len(list) / 32))
    return chunks


def buildargs(chunks):
    for i in range(32):
        yield [chunks[i]]



if __name__ == '__main__':

    subreddits = query_init()
    chunk = chunk(subreddits)
    chunks = []
    for i in range(32):
        if i != 31:
            chunks.append(subreddits[chunk * i:chunk * (i + 1)])
        else:
            chunks.append(subreddits[chunk * i:])

    with mp.Pool(processes=32) as pool:
        # args = buildargs(chunks)
        results = pool.starmap(find_depth, list(buildargs(chunks)))
        lengths = []
        reds = []
        counter = Counter()
        for res in results:
            for elem in res:
                counter[elem[0]] = elem[1]
        print(counter.most_common(10))
    print("--- %s seconds ---" % (time.time() - start_time))