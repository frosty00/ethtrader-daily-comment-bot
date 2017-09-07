#!/usr/bin/python3
import requests
import re

import praw
import demjson
from bs4 import BeautifulSoup

from imgurapi import get_gif
import mysql_wrapper

def querycmc():
    return demjson.decode(requests.get('https://coinmarketcap-nexuist.rhcloud.com/api/eth').text, decode_float=float)


def get_transaction_count():
    soup = BeautifulSoup(requests.get('https://etherscan.io/').text, "html.parser")
    script = soup.findAll('script')[3].string
    line = demjson.decode(re.search('data: (\[.*\])',  script, flags=re.MULTILINE).group(1))
    return line[-1]['y']


def select_phrase(change):
    if change < -5:
        return phrases[0]
    elif change < 5:
        return phrases[1]
    elif change < 10:
        return phrases[2]
    else:
        return phrases[3]

phrases = ['Hodl onto to your hats boys, it looks like we\'re at ${}',
           'Oh look at that, we\'re still at around ${}',
           'Nice, we\'re up to ${} today!',
           '#${} - TO THE [MOON](' + get_gif('moon') + ')']


footer = 'I\'m a bot, *bleep, bloop* | [source_code](https://pastebin.com/7fNH0csF) |\
          [FAQ](https://www.reddit.com/r/ethtrader/comments/6uhayr/introducing_a_new_ethereum_analytics_bot/) |\
          [hodl](https://www.ethhodler.org/) | /u/jadenpls'

reddit = praw.Reddit('bot1', user_agent='python')
ethtrader = reddit.subreddit('ethtrader')
daily = max((i.created_utc, i) for i in ethtrader.hot(limit=2) if i.stickied and 'Daily' in i.title)[1]

d = querycmc()
price, volume, marketcap = map(int, (d['price']['usd'], d['volume']['usd'], d['market_cap']['usd']))
transactions = get_transaction_count()
phrase = select_phrase(float(d['change'])).format(str(round(price, -1)))

try:
    newaths = mysql_wrapper.save_data((price, volume, marketcap, transactions))
except IntegrityError:
    raise RuntimeError('You have already commented in the last 24 hours')

athannounce = ''
for ath in newaths:
    athannounce += '\n\n#NEW {} ALL TIME HIGH OF {:,}!'.format(ath[0].upper(), ath[1])

daily.reply(
              phrase + '\n\n*Guess I\'ll check the price tomorrow...*' + athannounce + '\n\n---\n\n'
              + ''.join(' ^^'+w if w[0] != '*' else ' *'+'^^'+w[1:] for w in footer.split())
            )

print('Wrote comment successfully.')

