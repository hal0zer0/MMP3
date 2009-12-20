import gtk
import datetime
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.oggvorbis import OggVorbis
from mutagen.flac import FLAC
## DEBUG imports
import os

class Playlist(gtk.ListStore):
  def __init__(self):
    super(Playlist, self).__init__(str, str, str, str, str)
    self.total_length_seconds = 0
    self._DEBUG_add_fake_list()


  def add_column(self, name, id, treeView):
    rendererText = gtk.CellRendererText()
    #Allow Artist and Title fields to be editable by user
    if (name == "Title") or (name == "Artist"):
      rendererText.set_property('editable', True)
    rendererText.connect('edited', self.cell_edited_cb, id)
    column = gtk.TreeViewColumn(name, rendererText, text=id)
    column.set_resizable(True)
    column.set_reorderable(True)
    column.set_sort_column_id(id)

    treeView.append_column(column)


  def add_track(self, filenameToAdd):
    print "in playlist.add_track"
    

    #Verify file was selected, get extension and track info
    if filenameToAdd != None:
      ext = filenameToAdd.split(".").pop().lower()
      print "Extension is", ext
      #MP3 handler
      trackInfo = self._get_trackInfo(filenameToAdd, ext)
      self.append(trackInfo)
      self.update_track_numbers()

      
  


  def _get_trackInfo(self, filename, ext):

    try:
      if ext == "flac":
        track = FLAC(filename)
        length_seconds = track.info.length
      elif ext == "mp3":
        track = EasyID3(filename)
        fileInfo = MP3(filename)
        length_seconds = fileInfo.info.length

      elif ext == "ogg":
        track = OggVorbis(filename)
        length_seconds = track.info.length
      else:
        raise NotImplementedError
        return False
    except Exception as err:
      print err
      length_seconds = 0
      return [len(self) + 1, "Unknown", "Unknown", "0:00", filename]

    print track
    print length_seconds
    artist = track["artist"][0].strip()
    title = track["title"][0].strip()
    #length_seconds = flacInfo.info.length
    length_minutes = str(datetime.timedelta(seconds=int(length_seconds)))
    self.total_length_seconds += length_seconds

    return [len(self) + 1, title, artist, length_minutes, filename]

  def update_track_numbers(self):
    i = 1
    for line in self:
      line[0] = str(i).zfill(2)
      i += 1


  def remove_item(self, model, it):
    model.remove(it)
    self.update_track_numbers()


  def cell_edited_cb(self, cell, path, new_text, column):
    self[path][column] = new_text
    return

  def get_length(self):
    print self.total_length_seconds
    return datetime.timedelta(seconds=self.total_length_seconds)


  def _DEBUG_add_fake_list(self):
    i = 1
    for file in os.listdir("/mnt/media/Music/Tom Waits/Orphans (2006)/Bastards/"):
      self.add_track("/mnt/media/Music/Tom Waits/Orphans (2006)/Bastards/" + file)

author__= "Josh Price"