#!/usr/bin/python3
import praw
from forever import forever

reddit = praw.Reddit('bot1', user_agent='python')

for message in reddit.inbox.stream():
    print(message.body)
    comment_id = message.body.splitlines()[0]
    if message.subject == 'delete' and reddit.comment(comment_id).ups < 3:
        reddit.comment(comment_id).delete()

