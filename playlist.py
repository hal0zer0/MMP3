import gtk
import add_file_dialog
import datetime

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3



class Playlist(gtk.ListStore):
  def __init__(self):
    super(Playlist, self).__init__(str, str, str, str, str)


  def add_track(self):
    print "in playlist.add_track"
    filenameToAdd = add_file_dialog.show()
    ext = filenameToAdd[-3:].lower()
    print "Extension is", ext
    if (filenameToAdd != None) and  (ext == "mp3"):
      trackInfo = self._get_mp3_trackInfo(filenameToAdd)
      print "Appending", trackInfo
      self.append(trackInfo)
      #self.append(["99", "Artist", "Song",  "0:00", filenameToAdd])

  def _get_mp3_trackInfo(self, filename):
    return ["99", "Boogie Down", "Yourmomtones", "4:20", "/home"]





author__="Josh Price"