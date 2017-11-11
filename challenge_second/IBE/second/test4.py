SELECT DISTINCT t1.subreddit_id, t2.subreddit_id, COUNT(*)
             FROM comments t1, comments t2
             WHERE t1.subreddit_id <> t2.subreddit_id
             AND t2.subreddit_id < t1.subreddit_id
             AND t1.author_id = t2.author_id
             GROUP BY t1.author_id, t2.author_id
             ORDER BY COUNT(DISTINCT t1.author_id, t2.author_id )
             DESC
             LIMIT 10""