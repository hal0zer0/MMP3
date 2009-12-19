
import gtk

def show():
  #Verify GTK version
  if gtk.pygtk_version < (2,3,90):
    main.mmp2log(__name__,"PyGtk 2.3.90 or later required")
    raise SystemExit

  dialog = gtk.FileChooserDialog("Add a File",
                                None,
                                gtk.FILE_CHOOSER_ACTION_OPEN,
                                (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                  gtk.STOCK_OPEN, gtk.RESPONSE_OK))
  dialog.set_default_response(gtk.RESPONSE_OK)

  #Set up file filters...
  filter = gtk.FileFilter()
  filter.set_name("Supported Types")
  filter.add_pattern("*.m3u")
  dialog.add_filter(filter)

  filter = gtk.FileFilter()
  filter.set_name("All files")
  filter.add_pattern("*")
  dialog.add_filter(filter)

  response = dialog.run()
  if response == gtk.RESPONSE_OK:
    toreturn = dialog.get_filename()
    dialog.destroy()
    return toreturn
  else:
    dialog.destroy()
    return None

__author__= "Josh Price"