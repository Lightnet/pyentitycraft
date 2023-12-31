# Testing
"""
  Application Network test

  https://discourse.panda3d.org/t/panda3d-network-example/908/2
  https://docs.panda3d.org/1.10/python/programming/gui/rendering-text
  https://docs.panda3d.org/1.10/python/programming/networking/index

"""
import sys
from panda3d.core import WindowProperties

from direct.showbase.ShowBase import ShowBase

from direct.gui.DirectGui import DirectButton
from direct.gui.OnscreenText import OnscreenText

from panda3d.core import QueuedConnectionManager
from panda3d.core import QueuedConnectionListener
from panda3d.core import QueuedConnectionReader
from panda3d.core import ConnectionWriter
from panda3d.core import PointerToConnection
from panda3d.core import NetAddress

# network data
from panda3d.core import NetDatagram
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
# task
from direct.task import Task

# Developer-defined constants, telling the server what to do.
# Your style of how to store this information may differ; this is
# only one way to tackle the problem
PRINT_MESSAGE = 1

# APP
class Game(ShowBase):
  def __init__(self):
    ShowBase.__init__(self)

    wp = WindowProperties()
    wp.setTitle('py network')
    self.win.requestProperties(wp)
    
    self.build_ui()

  def build_ui(self):
    self.textNetwork = OnscreenText(text='Network', pos=(0.0, 0.0), scale=0.07)

    self.btn_host = DirectButton(text=("HOST"),scale=0.07, command=self.btn_server_host)
    self.btn_host.setPos(0.95,0,-0.95)
    
    self.btn_join = DirectButton(text=("JOIN"),scale=0.07, command=self.btn_client_join)
    self.btn_join.setPos(-0.95,0,-0.95)
    #pass

  def debuild_ui(self):
    self.btn_host.destroy()
    self.btn_join.destroy()
    self.textNetwork.destroy()
    #pass

  def btn_server_host(self):
    print("host")

    self.textObject = OnscreenText(text='Server', pos=(-0.5, 0.02), scale=0.07)

    self.btn_server_ping = DirectButton(text=("Ping"),scale=0.07, command=self.btn_host_ping)

    self.debuild_ui()
    self.cManager = QueuedConnectionManager()
    self.cListener = QueuedConnectionListener(self.cManager, 0)
    self.cReader = QueuedConnectionReader(self.cManager, 0)
    self.cWriter = ConnectionWriter(self.cManager, 0)

    self.activeConnections = [] # We'll want to keep track of these later

    self.port_address = 9099 #No-other TCP/IP services are using this port
    self.backlog = 1000 #If we ignore 1,000 connection attempts, something is wrong!
    self.tcpSocket = self.cManager.openTCPServerRendezvous(self.port_address,self.backlog)

    self.cListener.addConnection(self.tcpSocket)

    taskMgr.add(self.tskListenerPolling, "Poll the connection listener", -39)
    taskMgr.add(self.tskReaderPolling, "Poll the connection reader", -40)
    #pass

  def tskListenerPolling(self, taskdata):
    if self.cListener.newConnectionAvailable():
      print("polling...")
      rendezvous = PointerToConnection()
      netAddress = NetAddress()
      newConnection = PointerToConnection()

      if self.cListener.getNewConnection(rendezvous,netAddress,newConnection):
        print("connect...")
        newConnection = newConnection.p()
        self.activeConnections.append(newConnection) # Remember connection
        self.cReader.addConnection(newConnection)     # Begin reading connection
    return Task.cont

  def btn_host_close(self):
    # terminate connection to all clients
    for aClient in self.activeConnections:
      self.cReader.removeConnection(aClient)
    self.activeConnections = []
    # close down our listener
    self.cManager.closeConnection(self.tcpSocket)
    pass

  # MESSAGE DATA
  def myNewPyDatagram(self):
    # Send a test message
    myPyDatagram = PyDatagram()
    myPyDatagram.addUint8(PRINT_MESSAGE)
    myPyDatagram.addString("Hello, world!")
    return myPyDatagram

  def btn_host_ping(self):
    # broadcast a message to all clients
    myPyDatagram = self.myNewPyDatagram()  # build a datagram to send
    for aClient in self.activeConnections:
      self.cWriter.send(myPyDatagram, aClient)
    #pass

  def myProcessDataFunction(self,netDatagram):
    myIterator = PyDatagramIterator(netDatagram)
    msgID = myIterator.getUint8()
    if msgID == PRINT_MESSAGE:
        messageToPrint = myIterator.getString()
        print("server: ",messageToPrint)

  def tskReaderPolling(self,taskdata):
    if self.cReader.dataAvailable():
      print("dataAvailable...")
      datagram = NetDatagram()  # catch the incoming data in this instance
      # Check the return value; if we were threaded, someone else could have
      # snagged this data before we did
      if self.cReader.getData(datagram):
        print("getdata...")
        self.myProcessDataFunction(datagram)
        #pass
    return Task.cont

  def btn_client_join(self):
    self.debuild_ui()
    print("join")

    self.textObject = OnscreenText(text='Client', pos=(-0.5, 0.02), scale=0.07)
    self.btn_client_ping = DirectButton(text=("Ping"),scale=0.07, command=self.btn_client_ping)

    self.cManager = QueuedConnectionManager()
    self.cReader = QueuedConnectionReader(self.cManager, 0)
    self.cWriter = ConnectionWriter(self.cManager, 0)

    self.ip_address = '127.0.0.1'
    self.port_address = 9099
    self.timeout = 3000  # 3 seconds

    self.myConnection = self.cManager.openTCPClientConnection(self.ip_address, self.port_address, self.timeout)
    if self.myConnection:
      print("127.0.0.1...")
      self.cReader.addConnection(self.myConnection)  # receive messages from server
      #taskMgr.add(readClientTask, "serverReaderPollTask", -39)
      taskMgr.add(self.readClientTask, "serverReaderPollTask", -39)
    #pass

  def readClientTask(self, task):
    if self.cReader.dataAvailable():
      print("dataAvailable...")
      datagram = NetDatagram()  # catch the incoming data in this instance
      # Check the return value; if we were threaded, someone else could have
      # snagged this data before we did
      if self.cReader.getData(datagram):
        print("getdata...")
        self.myProcessDataFunction(datagram)

    return Task.cont

  def btn_client_close(self):
    self.cManager.closeConnection(self.myConnection)

  def btn_client_ping(self):
    myPyDatagram = self.myNewPyDatagram()  # build a datagram to send
    print("client...")
    self.cWriter.send(myPyDatagram, self.myConnection)

if __name__ == "__main__":
  try:
    game = Game()
    game.run()
  except OSError as err:
    print("OS error:", err)
  except ValueError:
    print("Oops!  That was no valid number.  Try again...")
    print(ValueError)
  except Exception as err:
    print(f"Unexpected {err=}, {type(err)=}")
    raise