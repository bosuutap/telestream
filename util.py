from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from more_itertools import chunked
import os, shelve

def albums():
    albums_list = os.listdir("albums")
    if not albums_list:
        return InlineKeyboardMarkup([[InlineKeyboardButton("Không có bộ sưu tập nào cả", url="https://www.google.com")], [InlineKeyboardButton("Xem danh sách album", callback_data="albums-button")]])
    albums_list = [album.replace(".album", "") for album in albums_list if album.endswith(".album")]
    chunked_keys = list(chunked(albums_list, 1))
    albums = []
    for chunk in chunked_keys:
        row_buttons = [InlineKeyboardButton(pre, callback_data=pre) for pre in chunk]
        albums.append(row_buttons)
    return InlineKeyboardMarkup(albums)

def album(name):
    if name.endswith(".album"):
        db = shelve.open(f"albums/{name}")
    else:
        db = shelve.open(f"albums/{name}.album")
    allkeys = list(db.keys())
    if not allkeys:
        return InlineKeyboardMarkup([[InlineKeyboardButton("Không có gì trong bộ sưu tập này", url="https://www.google.com")], [InlineKeyboardButton("Xem danh sách album", callback_data="albums-button")]])
    chunked_keys = list(chunked(allkeys, 3))
    album = []
    for chunk in chunked_keys:
        row_buttons = [InlineKeyboardButton(pre, callback_data=pre) for pre in chunk]
        album.append(row_buttons)
    album.append([InlineKeyboardButton("Xem danh sách album", callback_data="albums-button")])
    return InlineKeyboardMarkup(album)
    
def add_media(name, media):
    db = shelve.open(f"albums/{name}.album")
    db[media[0]]=media[1]
    
def del_media(name, media):
    db = shelve.open(f"albums/{name}.album")
    del db[media]
    
def get_media(name, media):
    db = shelve.open(f"albums/{name}.album")
    return db[media]