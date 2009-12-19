import gtk
import add_file_dialog
import datetime

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

#from ogg import vorbis
from mutagen.oggvorbis import OggVorbis

from mutagen.flac import FLAC



class Playlist(gtk.ListStore):
  def __init__(self):
    super(Playlist, self).__init__(str, str, str, str, str)


  def add_column(self, name, id, treeView):
    rendererText = gtk.CellRendererText()
    if (name == "Title") or (name == "Artist"):
      rendererText.set_property('editable', True)
    #rendererText.connect('edited', self.edited_cb, (self.store, iter))
    column = gtk.TreeViewColumn(name, rendererText, text=id)
    column.set_resizable(True)
    column.set_reorderable(True)
    column.set_sort_column_id(id)
    treeView.append_column(column)


  def add_track(self):
    print "in playlist.add_track"
    filenameToAdd = add_file_dialog.show()

    #Verify file was selected, get extension and track info
    if filenameToAdd != None:
      ext = filenameToAdd.split(".").pop().lower()
      print "Extension is", ext
      #MP3 handler
      if ext == "mp3":
        trackInfo = self._get_mp3_trackInfo(filenameToAdd)
        self.append(trackInfo)
        self._update_track_numbers()
        return True
      #FLAC handler
      elif ext == "flac":
        trackInfo = self._get_flac_trackInfo(filenameToAdd)
        self.append(trackInfo)
        self._update_track_numbers()
        return True
      elif ext == "ogg":
        trackInfo = self._get_ogg_trackInfo(filenameToAdd)
        self.append(trackInfo)
        self._update_track_numbers()
        return True

      else:
        return False

    


  def _get_flac_trackInfo(self, filename):
    try:
      flacInfo = FLAC(filename)
      print flacInfo
      print flacInfo.info.length
      artist = flacInfo["artist"][0].strip()
      title = flacInfo["title"][0].strip()
      length = str(datetime.timedelta(seconds=int(flacInfo.info.length)))
    except Exception as err:
      print err
      artist = "Unknown"
      title = "Unknown"
      length = "0:00"
      
    return [len(self) + 1, title, artist, length, filename]


  def _get_ogg_trackInfo(self, filename):
    try:
      oggInfo = OggVorbis(filename)
      print oggInfo
      print oggInfo.info.length
      artist = oggInfo["artist"][0].strip()
      title = oggInfo["title"][0].strip()
      length = str(datetime.timedelta(seconds=int(oggInfo.info.length)))
    except Exception as err:
      print err
      artist = "Unknown"
      title = "Unknown"
      length = "0:00"

    return [len(self) + 1, title, artist, length, filename]


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


  def remove_item(self, model, it):
    model.remove(it)
    self._update_track_numbers()

author__= "Josh Price"