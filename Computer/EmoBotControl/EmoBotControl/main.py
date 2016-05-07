#! /usr/bin/env python
# -*- coding: utf-8 -*-

import about
import cv2
import numpy as np
import socket
import SocketServer
import threading

import wx
from wx.lib.pubsub import pub


class VideoStreamHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        stream_bytes = ' '

        # stream video frames one by one
        try:
            while True:
                stream_bytes += self.rfile.read(1024)
                first = stream_bytes.find('\xff\xd8')
                last = stream_bytes.find('\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),
                                         cv2.CV_LOAD_IMAGE_UNCHANGED)

                    cv2.imshow('image', image)

        finally:
            cv2.destroyAllWindows()


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


class ThreadServer(object):

    def __init__(self):
        # Port 0 means to select an arbitrary unused port
        HOST, PORT = "localhost", 2016

        server = ThreadedTCPServer((HOST, PORT), VideoStreamHandler)
        ip, port = server.server_address

        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()

        print "Server loop running in thread:", server_thread.name
        print 'Starting up TCP on {0} port {1}'.format(ip, port)



class SocketThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

        self.server_address = ('localhost', 2016)
        print 'starting up on %s port %s' % self.server_address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.server_address)
        self.sock.listen(1)

        self.setDaemon(True)
        self.start()

    def run(self):
        """
        Run the socket "server"
        """
        while True:
            try:
                # Wait for a connection
                print 'waiting for a connection'
                client, addr = self.sock.accept()
                print 'connection from', addr

                received = client.recv(4096)
                wx.CallAfter(pub.sendMessage, "panelListener", message=received)

            except socket.error, err:
                print "Socket error! %s" % err
                break

        # shutdown the socket
        try:
            self.sock.shutdown(socket.SHUT_RDWR)

        except:
            pass

        self.sock.close()


class MainPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.SetFocus()


class MainFrame(wx.Frame):

    def __init__(self, parent, title):
        super(MainFrame, self).__init__(parent, title=title,
                                        size=(720, 640))

        # Start TCP thread server
        ThreadServer()
        pub.subscribe(self.receivedMessage, "panelListener")

        self.SetIcon(wx.Icon("images/icon.png"))
        self.panel = MainPanel(self)
        self.statusbar = self.CreateStatusBar()
        self.InitUI()

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

    def receivedMessage(self, message):
        """
        Listener function
        """
        print "Received the following message: " + message
        self.statusbar.SetStatusText("Received the following message: " + message)

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
            self.client.connect(('localhost', 2015))
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