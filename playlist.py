import gtk
import add_file_dialog

__author__="Josh Price"

class Playlist(gtk.ListStore):
  def __init__(self):
    super(Playlist, self).__init__(str, str, str, str, str)


  def add_track(self, filename):
    filenameToAdd = add_file_dialog.show()
    self.append(["99", "Artist", "Song", filenameToAdd, "0:00"])