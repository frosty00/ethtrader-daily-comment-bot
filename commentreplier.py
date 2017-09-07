#!/usr/bin/python3
import re
from urllib import parse

import praw

from imgurapi import get_gif
from forever import forever

regex = r'(?<!( buy|long) or )(sell|short)(ing)?\s(?!(/ |or )?(buy|long))(.{0,16})\beth(ereum|er)?\b.{0,16}[?]'
BOT_NAME = 'should_i_sell_my_eth'
BOT_NAME = 'jadenpls'
reddit = praw.Reddit('bot1', user_agent='python')
ethtrader = reddit.subreddit('ethtrader')

footer = 'I\'m a bot, *bleep, bloop* | [source_code](https://pastebin.com/MZLsPdVJ) |\
          [submit_meme](https://www.reddit.com/message/compose/?to=jadenpls&subject=submit%20meme&message=send%20me%20a%20meme) |\
          [delete]({}) | [inspiration](http://www.shouldisellmybitcoins.com/) |\
          [hodl](https://www.ethhodler.org/) | /u/jadenpls'


@forever
def main():
    for comment in ethtrader.stream.comments():
        print('Processing:', comment, comment.body)
        match = re.search(regex, comment.body.lower())

        if match:
            try:
                comment.refresh()
            except praw.exceptions.ClientException:  # fix for deleted comments
                print('SKIPPING due to clientexcep:', comment, comment.body)
                continue
            print('Caught:', comment, comment.body)
            already_replied = any(c.author == BOT_NAME for c in comment.replies)
            print('ALREADY REPLIED: {}\nREPLIES: {}'.format(already_replied, ',\n'.join(c.body for c in comment.replies)))
            if not already_replied:
                print('REPLYING')
                reply = comment.reply('.')
                params = {'to': BOT_NAME, 'subject': 'delete', 'message': '{}\n\nINPUT: "{}"'.format(reply.id, comment.body)}
                delete_link = parse.urljoin('https://www.reddit.com/message/compose/', '?'+parse.urlencode(params))
                reply.edit('[hmm lemme think about that...]({})'.format(get_gif('no'))
                           + '\n\n---\n\n'
                           + ''.join(' ^^' + w if w[0] != '*' else ' *'+'^^'+w[1:]
                                     for w in footer.format(delete_link).split()))


main()

