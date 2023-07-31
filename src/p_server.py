

from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties

from panda3d.core import QueuedConnectionManager
from panda3d.core import QueuedConnectionListener
from panda3d.core import QueuedConnectionReader
from panda3d.core import ConnectionWriter
from panda3d.core import PointerToConnection
from panda3d.core import NetAddress

from panda3d.core import NetDatagram

from direct.task import Task

cManager = QueuedConnectionManager()
cListener = QueuedConnectionListener(cManager, 0)
cReader = QueuedConnectionReader(cManager, 0)
cWriter = ConnectionWriter(cManager, 0)

activeConnections = [] # We'll want to keep track of these later

port_address = 9099 #No-other TCP/IP services are using this port
backlog = 1000 #If we ignore 1,000 connection attempts, something is wrong!
tcpSocket = cManager.openTCPServerRendezvous(port_address,backlog)

cListener.addConnection(tcpSocket)

def tskListenerPolling(taskdata):
    if cListener.newConnectionAvailable():
        print("polling...")
        rendezvous = PointerToConnection()
        netAddress = NetAddress()
        newConnection = PointerToConnection()

        if cListener.getNewConnection(rendezvous,netAddress,newConnection):
            print("connect...")
            newConnection = newConnection.p()
            activeConnections.append(newConnection) # Remember connection
            cReader.addConnection(newConnection)     # Begin reading connection
    return Task.cont

def tskReaderPolling(taskdata):
    if cReader.dataAvailable():
        print("dataAvailable...")
        datagram = NetDatagram()  # catch the incoming data in this instance
        # Check the return value; if we were threaded, someone else could have
        # snagged this data before we did
        if cReader.getData(datagram):
            print("getdata...")
            #myProcessDataFunction(datagram)
            pass
    return Task.cont


#taskMgr.add(tskListenerPolling, "Poll the connection listener", -39)
#taskMgr.add(tskReaderPolling, "Poll the connection reader", -40)

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        #properties = WindowProperties()
        #properties.setSize(1000, 750)
        #self.win.requestProperties(properties)

        #print("taskMgr: ", taskMgr)
        taskMgr.add(tskListenerPolling, "Poll the connection listener", -39)
        taskMgr.add(tskReaderPolling, "Poll the connection reader", -40)
        print("init server...")

game = Game()
game.run()