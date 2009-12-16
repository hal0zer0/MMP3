import gtk
import playlist

__author__="Josh Price"

class MMP3(gtk.Window):
  def __init__(self):
    super(MMP3, self).__init__()

    #Set initial window
    self.set_size_request(800, 600)
    self.set_position(gtk.WIN_POS_CENTER)
    self.connect("destroy", gtk.main_quit)
    self.set_title("MMP3")

    #Create 16x16 grid to hold window contents
    self.table = gtk.Table(16,16,True)

    #Create scrolling window to hold playlist
    sw = gtk.ScrolledWindow()
    sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
    sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    self.table.attach(sw, 0,16,0,14)

    #Insert custom Playlist class into treeview, add to scrolling window
    self.playlist = playlist.Playlist()
    self.treeView = gtk.TreeView(self.playlist)

    #Create initial columns in treeview
    initial_columns = ("#", "Title", "Artist", "Length", "Path")
    i = 0
    for cname in initial_columns:
      self.add_column(cname, i)
      i += 1
    sw.add(self.treeView)

    self.add(self.table)
    self.show_all()

  def add_column(self, name, iter):
    rendererText = gtk.CellRendererText()
    if (name == "Title") or (name == "Artist"):
      rendererText.set_property('editable', True)
    #rendererText.connect('edited', self.edited_cb, (self.store, iter))
    column = gtk.TreeViewColumn(name, rendererText, text=iter)
    column.set_sort_column_id(iter)
    self.treeView.append_column(column)
    iter += 1

if __name__ == "__main__":
  MMP3()
  gtk.main()