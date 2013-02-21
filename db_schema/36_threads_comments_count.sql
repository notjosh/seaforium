ALTER TABLE threads 
ADD COLUMN comments_count INT NOT NULL DEFAULT '1';

UPDATE threads
SET comments_count = (SELECT count(comments.comment_id)
        FROM comments
        WHERE comments.thread_id = threads.thread_id)
