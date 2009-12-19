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

    #Before processing, check to see if file was actually selected
    if filenameToAdd != None:
      #MP3 handler
      if ext == "mp3":
        trackInfo = self._get_mp3_trackInfo(filenameToAdd)
        self.append(trackInfo)
    self._update_track_numbers()

  def remove_item(self, model, it):
    model.remove(it)
    self._update_track_numbers()

  def _get_mp3_trackInfo(self, filename):
    #Get artist and title from ID3
    try:
      id3Info = EasyID3(filename)
      artist = id3Info["artist"][0].strip()
      title = id3Info["title"][0].strip()
    except Exception as err:
      print err
      artist = "Unknown"
      title = "Unknown"

    #Get length info from MP3 file
    try:
      file_info = MP3(filename)
      secondslong = int(file_info.info.length)
      length = str(datetime.timedelta(seconds=secondslong))
    except:
      length = "0:00"

    return [len(self) + 1, title, artist, length, filename]


  def _update_track_numbers(self):
    i = 1
    for line in self:
      line[0] = str(i).zfill(2)
      i += 1




author__="Josh Price"