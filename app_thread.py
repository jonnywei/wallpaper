from gi.repository import Gtk,Gdk, GLib,GObject
import threading 
import time

class App(Gtk.Window):

    def __init__(self):
        super(App, self).__init__()
        self.connect("destroy", self.on_destroy)

        self.layout = Gtk.VBox()
        self.progress = Gtk.ProgressBar()
        self.layout.pack_start(self.progress, False, False, 0)

        self.set_size_request(100,100)

        self.go_button = Gtk.Button("Start")
        self.go_button.connect("clicked", self.do_work)
        self.layout.pack_start(self.go_button, False, False, 0)

        self.add(self.layout)
        self.show_all()



    def on_destroy(widget, event):
        Gtk.main_quit()

    def do_work(self, widget):
        def worker_thread():
            so_far = 0
            while so_far < 10:
                time.sleep(0.5)
                print("work so far: %s" % so_far)
                Gdk.threads_enter()
                try:
                    if so_far > 0:
                        self.progress.set_fraction(so_far / 10.0)
                finally:
                    Gdk.threads_leave()
                so_far += 1
        threading.Thread(target=worker_thread).start()



if __name__ == "__main__":
    app = App()
    GObject.threads_init()
    Gdk.threads_init()
    Gdk.threads_enter()
    Gtk.main()
    Gdk.threads_leave()
