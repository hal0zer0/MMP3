import add_file_dialog
import gtk
import playlist
import publisher

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
    self.connect("destroy", gtk.main_quit)
    self.set_title("MMP3")

    #Create 16x16 grid to hold window contents
    self.table = gtk.Table(16,16,True)

    #Create scrolling window to hold playlist
    sw = gtk.ScrolledWindow()
    sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
    sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    self.table.attach(sw, 0,16,0,14)

    summaryText = "Nothin yet"
    summary = gtk.Label()
    summary.set_text(summaryText)
    self.table.attach(summary, 0, 8, 14, 15)

    #Insert custom Playlist class into treeview
    self.playlist = playlist.Playlist(summary)
    self.treeView = gtk.TreeView(self.playlist)
    self.treeView.set_reorderable(True)
    self.treeView.connect("cursor-changed", self.select_cb, self.treeView.get_selection())
    self.treeView.connect("drag-end", self.drop_cb)
    self.treeView.connect("key-press-event", self.key_press_cb)
    #self.treeView.connect("columns-changed", self.reorder_cb)

    #Create initial columns in treeview
    initial_columns = ("#", "Title", "Artist", "Length", "Path")
    i = 0
    for cname in initial_columns:
      self.playlist.add_column(cname, i, self.treeView)
      i += 1

    sw.add(self.treeView)

    #Now create and add buttons
    self.add_buttons()
    self.add(self.table)
    self.show_all()


  def add_buttons(self):
    self.addFileButton = gtk.Button("Add Item")
    self.addFileButton.connect("clicked", self.add_button_cb)
    self.table.attach(self.addFileButton, 0,2,15,16)

    #Del Item button
    self.addFileButton = gtk.Button("Del Item")
    self.addFileButton.connect("clicked", self.del_button_cb)
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
    self.addFileButton.connect("clicked", self.pub_button_cb)
    self.table.attach(self.addFileButton, 14,16,15,16)


  # Callback functions
  def add_button_cb(self, widget):
    filenameToAdd = add_file_dialog.show()
    self.playlist.add_track(filenameToAdd)


  def del_button_cb(self, widget):
    self.playlist.remove_item(self.model, self.it)


  def select_cb(self, widget, data=None):
    self.selection = data.get_selected()
    if self.selection: #result could be None
      self.model, self.it = self.selection


  def drop_cb(self, widget, data):
    self.playlist.update_view()
    

  def key_press_cb(self, arg1, key_pressed):
    #check for delete key
    if key_pressed.keyval == 65535:
      self.playlist.remove_item(self.model, self.it)

  def pub_button_cb(self, widget):
    pw = publisher.PublishWindow(self.playlist)
    
    
if __name__ == "__main__":
  MMP3()
  gtk.main()