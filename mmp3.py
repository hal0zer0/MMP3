import add_file_dialog
import gtk
import playlist

__author__="Josh Price"

class MMP3(gtk.Window):
  def __init__(self):
    #Verify GTK version
    if gtk.pygtk_version < (2,3,90):
      print "PyGtk 2.3.90 or later required"
      raise SystemExit

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

    #Now create and add buttons
    self.add_buttons()
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
    #iter += 1

  def add_buttons(self):
    self.addFileButton = gtk.Button("Add Item")
    self.addFileButton.connect("clicked", self.add_button_cb)
    self.table.attach(self.addFileButton, 0,2,15,16)

    #Del Item button
    self.addFileButton = gtk.Button("Del Item")
    self.addFileButton.connect("clicked", self.add_button_cb, "DEL")
    self.table.attach(self.addFileButton, 2,4,15,16)

    #Add Save button
    self.addFileButton = gtk.Button("Save List")
    self.addFileButton.connect("clicked", self.add_button_cb, "SAVE")
    self.table.attach(self.addFileButton, 12,14,15,16)

    #Load List button
    self.addFileButton = gtk.Button("Load List")
    self.addFileButton.connect("clicked", self.add_button_cb, "LOAD")
    self.table.attach(self.addFileButton, 10,12,15,16)

    #Publish List button
    self.addFileButton = gtk.Button("PUBLISH")
    self.addFileButton.connect("clicked", self.add_button_cb, "PUB")
    self.table.attach(self.addFileButton, 14,16,15,16)

  def add_button_cb(self, widget):
    print "Add button clcked"
    self.playlist.add_track(add_file_dialog.show())

  
if __name__ == "__main__":
  MMP3()
  gtk.main()