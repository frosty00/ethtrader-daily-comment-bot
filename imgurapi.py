#!/usr/bin/python3
from imgurpython import ImgurClient
from random import choice

client_id = '8a56c9986470323'
client_secret = '792feff61180ac7dbcbe25f89086c5106531a3e7'
refresh_token = 'fed535595bb117865133996c41b1863c3a1f6241'
client = ImgurClient(client_id, client_secret, refresh_token=refresh_token)


def get_gif(album):
    album_ids = {'moon': '0NG2b', 'no': 'X6qiH'}
    return choice([i.link for i in client.get_album_images(album_ids[album.lower()])])
