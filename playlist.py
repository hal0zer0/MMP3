import gtk

__author__="Josh Price"

class Playlist(gtk.ListStore):
  def __init__(self):
    super(Playlist, self).__init__(str)