
from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties

from panda3d.core import QueuedConnectionManager
from panda3d.core import QueuedConnectionListener
from panda3d.core import QueuedConnectionReader
from panda3d.core import ConnectionWriter
from panda3d.core import PointerToConnection
from panda3d.core import NetAddress

cManager = QueuedConnectionManager()
cListener = QueuedConnectionListener(cManager, 0)
cReader = QueuedConnectionReader(cManager, 0)
cWriter = ConnectionWriter(cManager, 0)

activeConnections = [] # We'll want to keep track of these later
port_address = 9099  # same for client and server

# A valid server URL. You can also use a DNS name
# if the server has one, such as "localhost" or "panda3d.org"
#ip_address = "192.168.0.50"
ip_address = '127.0.0.1'

# How long, in milliseconds, until we give up trying to reach the server?
timeout = 3000  # 3 seconds

myConnection = cManager.openTCPClientConnection(ip_address, port_address, timeout)
if myConnection:
    print("127.0.0.1...")
    cReader.addConnection(myConnection)  # receive messages from server


class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        #properties = WindowProperties()
        #properties.setSize(1000, 750)
        #self.win.requestProperties(properties)

        taskMgr.add(readTask, "serverReaderPollTask", -39)



game = Game()
game.run()
