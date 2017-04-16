import os
import sys
import urllib
import eyed3
from goldfinch import validFileName as vfn
from gmusicapi import Mobileclient

if len(sys.argv) == 1:
  print "usage: python google-music-downloader.py <login> <password> <target directory> <album id>"
  sys.exit()

login = sys.argv[1]
password = sys.argv[2]
targetDir = sys.argv[3]
albumId = sys.argv[4]

eyed3.log.setLevel("ERROR")

api = Mobileclient(debug_logging=False)
api.login(login, password, Mobileclient.FROM_MAC_ADDRESS)

album = api.get_album_info(albumId)
dirName = vfn("%s - %s" % (album["artist"], album["name"]), space="keep", initCap=False)
dirPath = targetDir + "/" + dirName

print("downloading to directory: " + dirPath)
if not os.path.exists(dirPath):
    os.makedirs(dirPath)
	
for song in album["tracks"]:
  url = api.get_stream_url(song_id=song["storeId"], quality="hi")
  fileName = vfn("%s. %s - %s.mp3" % (song["trackNumber"], song["artist"], song["title"]), space="keep", initCap=False)
  filePath = dirPath + "/" + fileName
  print("downloading: " + fileName)
  urllib.urlretrieve(url, filePath)
  
  audio = eyed3.load(filePath)
  if audio.tag is None:
    audio.tag = eyed3.id3.Tag()
    audio.tag.file_info = eyed3.id3.FileInfo(filePath)
  audio.tag.artist = song["artist"]
  audio.tag.album = album["name"]
  audio.tag.album_artist = album["artist"]
  audio.tag.title = song["title"]
  audio.tag.track_num = song["trackNumber"]
  audio.tag.save()

print("done.")
