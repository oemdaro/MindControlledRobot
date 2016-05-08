#! /usr/bin/env python
# -*- coding: utf-8 -*-

import SocketServer
import socket
import threading

import cv2
import numpy as np
import wx

import about


class VideoStreamHandler(SocketServer.StreamRequestHandler):

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

                    cv2.imwrite('images/stream.jpg', image)

        finally:
            cv2.destroyAllWindows()


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


class ThreadServer(object):

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


class MainPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.SetFocus()


class MainFrame(wx.Frame):

    def __init__(self, parent, title):
        super(MainFrame, self).__init__(parent, title=title,
                                        size=(656, 562))

        # Start TCP thread server
        self.threadServer = ThreadServer()

        self.SetIcon(wx.Icon("images/icon.png"))
        self.panel = MainPanel(self)
        self.statusbar = self.CreateStatusBar()
        self.InitUI()

        # timer setup
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnShowVideo)
        self.timer.Start(100)

        self.Centre()
        self.Show(True)

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
        self.panel.Bind(wx.EVT_KEY_DOWN, self.KeyboardCatch)

        self.statusbar.SetStatusText('Ready')

    def OnShowVideo(self, event):
        img_out = wx.Image('images/stream.jpg')
        bitmap_in = img_out.ConvertToBitmap()
        wx.StaticBitmap(self, -1, bitmap_in, (0, 0), self.Fit())

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
            self.client.connect(('192.168.1.13', 2015))
            self.client.sendall(message)
            self.statusbar.SetStatusText("Send the following message: " + message)

        except socket.error, err:

            self.statusbar.SetStatusText('Please start TCP server before running GUI. ' + \
                                         'The command out is not working')
            print err

        except Exception, exc:
            print exc

        finally:
            self.client.close()

        e.Skip()

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
    MainFrame(None, title='EmoBotControl')
    app.MainLoop()
