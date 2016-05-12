import SocketServer
import socket
import threading

import cv2
import numpy as np
import wx
from wx.lib.pubsub import pub

import about


class VideoStreamHandler(SocketServer.StreamRequestHandler):
    """docstring for ShowCapture"""

    def handle(self):
        stream_bytes = ' '

        # stream video frames one by one
        try:
            while True:
                stream_bytes += self.rfile.read(2048)
                first = stream_bytes.find('\xff\xd8')
                last = stream_bytes.find('\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),
                                         cv2.IMREAD_UNCHANGED)

                    wx.CallAfter(pub.sendMessage, "panelListener", image=image)

        finally:
            cv2.destroyAllWindows()


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """docstring for ShowCapture"""
    pass


class ThreadServer(object):
    """docstring for ShowCapture"""

    def __init__(self):
        # Port 0 means to select an arbitrary unused port
        HOST, PORT = "0.0.0.0", 2016

        self.server = ThreadedTCPServer((HOST, PORT), VideoStreamHandler)
        ip, port = self.server.server_address

        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=self.server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()

        print "Server loop running in thread:", server_thread.name
        print 'Starting up TCP Server. Server listening on {0} port {1}'.format(ip, port)


class ShowCapture(wx.Panel):
    """docstring for ShowCapture"""

    def __init__(self, parent, fps=15):
        wx.Panel.__init__(self, parent)

        self.parent = parent
        self.width, self.height = 640, 480
        self.parent.SetSize((self.width, self.height))
        self.fps = fps

        pub.subscribe(self.ReceivedImage, "panelListener")

        self.SetFocus()

    def ReceivedImage(self, image):
        # print "Received image..."
        self.capture = image
        frame = self.capture
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.bmp = wx.BitmapFromBuffer(self.width, self.height, frame)

        self.timer = wx.Timer(self)
        self.timer.Start(1000./self.fps)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.NextFrame)
        self.Bind(wx.EVT_KEY_DOWN, self.KeyboardCatch)

    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0)

    def NextFrame(self, event):
        frame = self.capture
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.bmp.CopyFromBuffer(frame)
        self.Refresh()

    def KeyboardCatch(self, e):
        keycode = e.GetKeyCode()
        print keycode
        message = ""
        if keycode == 65:
            message = "a"
        elif keycode == 68:
            message = "d"
        elif keycode == 87:
            message = "w"
        elif keycode == 83:
            message = "s"
        else:
            message = "Unknown command."

        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(('raspberrypi.mshome.net', 2015))
            self.client.sendall(message)
            self.parent.statusbar.SetStatusText("Send the following message: " + message)

        except socket.error, err:
            self.parent.statusbar.SetStatusText('Please start TCP server before running GUI. ' + \
                                         'The command out is not working')
            print err

        except Exception, exc:
            print exc

        finally:
            self.client.close()


class MainFrame(wx.Frame):
    """docstring for MainFrame"""
    def __init__(self, parent, title):
        super(MainFrame, self).__init__(parent, title=title)

        self.threadServer = ThreadServer()
        self.SetIcon(wx.Icon("images/icon.png"))
        self.statusbar = self.CreateStatusBar()
        self.InitUI()

    def InitUI(self):
        menubar = wx.MenuBar()

        fileMenu = wx.Menu()
        fitem = wx.MenuItem(fileMenu, wx.ID_EXIT, 'Quit\tCtrl+Q', 'Quit application')
        fitem.SetBitmap(wx.Bitmap("images/exit.png"))
        fileMenu.AppendItem(fitem)

        helpMenu = wx.Menu()
        aboutitem = wx.MenuItem(helpMenu, wx.ID_ABORT, 'About\tCtrl+A', 'About EmoBotControl')
        aboutitem.SetBitmap(wx.Bitmap("images/about.png"))
        helpMenu.AppendItem(aboutitem)

        menubar.Append(fileMenu, '&File')
        menubar.Append(helpMenu, '&Help')
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.OnQuit, fitem)
        self.Bind(wx.EVT_MENU, self.OnAboutBox, aboutitem)

        self.statusbar.SetStatusText('Ready')

    def OnQuit(self, e):
        self.threadServer.server.shutdown()
        self.threadServer.server.server_close()
        self.Close()

    def OnAboutBox(self, e):
        description = about.description
        licence = about.licence

        info = wx.AboutDialogInfo()
        info.SetIcon(wx.Icon("images/icon.png", wx.BITMAP_TYPE_PNG))
        info.SetName('EmoBotControl')
        info.SetVersion('1.0')
        info.SetDescription(description)
        info.SetCopyright('(C) 2016 Daro Oem')
        info.SetWebSite('http://www.facebook.com/daro.oem')
        info.SetLicence(licence)
        info.AddDeveloper('Daro Oem')

        wx.AboutBox(info)

if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame(None, title='EmoBotControl')
    frame.Centre()
    cap = ShowCapture(frame)
    frame.Show()
    app.MainLoop()
