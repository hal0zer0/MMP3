import gtk
import datetime
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.oggvorbis import OggVorbis
from mutagen.flac import FLAC
## DEBUG imports
import os


class Playlist(gtk.ListStore):
  def __init__(self, summary):
    super(Playlist, self).__init__(str, str, str, str, str, float)
    self.summary = summary
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
    #Verify file was selected, get extension and track info
    if filenameToAdd != None:
      ext = filenameToAdd.split(".").pop().lower()
      trackInfo = self._get_trackInfo(filenameToAdd, ext)
      self.append(trackInfo)
      self.update_view()

      
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
        #raise NotImplementedError
        return False
    except Exception as err:
      print err
      finalInfo = [len(self) + 1, "Unknown", "Unknown", "0:00", filename, 0]

      return finalInfo

    artist = track["artist"][0].strip()
    title = track["title"][0].strip()
    
    length_minutes = str(datetime.timedelta(seconds=int(length_seconds)))
    
    finalInfo =  [len(self) +1,   #add 1 to number of items in playlist
                 title,
                 artist,
                 length_minutes,
                 filename,
                 length_seconds]

    return finalInfo

  def update_view(self):
    #First assign track numbers to rows zero-padded
    #"self" is a ListStore so two-dimensional list
    i = 1
    total = 0
    for track in self:
      track[0] = str(i).zfill(2)
      total += track[5]
      i += 1
    minutes = str(datetime.timedelta(seconds=int(total)))
    numTracks = len(self)
    summaryText = "Tracks: %s    Total Running Time:  %s" % (numTracks, minutes)
    self.summary.set_text(summaryText)


  def remove_item(self, model, it):
    self.remove(it)
    self.update_view()


  def cell_edited_cb(self, cell, path, new_text, column):
    self[path][column] = new_text
    self.update_view()
    

  def _DEBUG_add_fake_list(self):
    print "FAKE DEBUG PLAYLIST GENERATION ENABLED"
    print "COMMENT OUT FROM BEGINNING OF PLAYLIST.PY TO DISABLE"
    print "THIS SHOULD NOT BE IN THE RELEASE FILE"
    i = 1
    for file in os.listdir("/mnt/media/Music/Tom Waits/Orphans (2006)/Bastards/"):
      self.add_track("/mnt/media/Music/Tom Waits/Orphans (2006)/Bastards/" + file)

author__= "Josh Price"