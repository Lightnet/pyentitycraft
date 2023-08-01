# p_network_repository
# https://github.com/panda3d/panda3d/blob/master/samples/networking/01-simple-connection/server.py
# https://docs.panda3d.org/1.10/cpp/programming/networking/distributed/index
# 

import argparse
# all imports needed by the engine itself
from direct.showbase.ShowBase import ShowBase

# all imports needed by the server
from direct.distributed.ServerRepository import ServerRepository
from panda3d.core import ConfigVariableInt

# initialize the client
from direct.distributed.ClientRepository import ClientRepository
from panda3d.core import URLSpec, ConfigVariableInt, ConfigVariableString
# ui
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode

#================================================
# SERVER CLASS
#================================================

# the main server class
class GameServerRepository(ServerRepository):
  """The server repository class"""
  def __init__(self):
    """initialise the server class"""

    # get the port number from the configuration file
    # if it doesn't exist, we use 4400 as the default
    tcpPort = ConfigVariableInt('server-port', 4400).getValue()

    # list of all needed .dc files
    dcFileNames = ['./direct.dc']

    # initialise a threaded server on this machine with
    # the port number and the dc filenames
    ServerRepository.__init__(self, tcpPort, dcFileNames=dcFileNames, threadedNet=True)

# server with AI
class AIRepository(ClientRepository):
    def __init__(self):
        """ The AI Repository usually lives on a server and is responsible for
        server side logic that will handle game objects """

        # List of all dc files that are of interest to this AI Repository
        dcFileNames = ['./direct.dc']

        # Initialize the repository.  We pass it the dc files and as this is an
        # AI repository the dcSuffix AI.  This will make sure any later calls to
        # createDistributedObject will use the correct version.
        # The connectMethod
        ClientRepository.__init__(
            self,
            dcFileNames = dcFileNames,
            dcSuffix = 'AI',
            threadedNet = True)

        # Set the same port as configured on the server to be able to connect
        # to it
        tcpPort = ConfigVariableInt('server-port', 4400).getValue()

        # Set the IP or hostname of the server we want to connect to
        hostname = ConfigVariableString('server-host', '127.0.0.1').getValue()

        # Build the URL from the server hostname and port. If your server
        # doesn't use http you should change it accordingly. Make sure to pass
        # the connectMethod to the  ClientRepository.__init__ call too.
        # Available connection methods are:
        # self.CM_HTTP, self.CM_NET and self.CM_NATIVE
        url = URLSpec('http://{}:{}'.format(hostname, tcpPort))

        # Attempt a connection to the server
        self.connect([url],
                     successCallback = self.connectSuccess,
                     failureCallback = self.connectFailure)

    def connectFailure(self, statusCode, statusString):
        """ something went wrong """
        print("Couldn't connect. Make sure to run server.py first!")
        raise(StandardError, statusString)

    def connectSuccess(self):
        """ Successfully connected.  But we still can't really do
        anything until we've got the doID range. """
        # The Client Repository will throw this event as soon as it has a doID
        # range and would be able to create distributed objects
        self.accept('createReady', self.gotCreateReady)

    def lostConnection(self):
        """ This should be overridden by a derived class to handle an
         unexpectedly lost connection to the gameserver. """
        exit()

    def gotCreateReady(self):
        """ Now we're ready to go! """

        # This method checks whether we actually have a valid doID range
        # to create distributed objects yet
        if not self.haveCreateAuthority():
            # Not ready yet.
            return

        # we are ready now, so ignore further createReady events
        self.ignore('createReady')

        # Create a Distributed Object by name.  This will look up the object in
        # the dc files passed to the repository earlier
        self.timeManager = self.createDistributedObject(
            className = 'TimeManagerAI', # The Name of the Class we want to initialize
            zoneId = 1) # The Zone this Object will live in

        print("AI Repository Ready")

    def deallocateChannel(self, doID):
        """ This method will be called whenever a client disconnects from the
        server.  The given doID is the ID of the client who left us. """
        print("Client left us: ", doID)

#================================================
# CLIENT CLASS
#================================================

# client
class GameClientRepository(ClientRepository):

    def __init__(self, base):
        self.base = base
        dcFileNames = ['./direct.dc']

        # a distributed object of our game.
        self.distributedObject = None
        self.aiDGameObect = None

        ClientRepository.__init__(
            self,
            dcFileNames = dcFileNames,
            threadedNet = True)

        # Set the same port as configured on the server to be able to connect
        # to it
        tcpPort = ConfigVariableInt('server-port', 4400).getValue()

        # Set the IP or hostname of the server we want to connect to
        hostname = ConfigVariableString('server-host', '127.0.0.1').getValue()

        # Build the URL from the server hostname and port. If your server
        # uses another protocol then http you should change it accordingly.
        # Make sure to pass the connectMethod to the  ClientRepository.__init__
        # call too.  Available connection methods are:
        # self.CM_HTTP, self.CM_NET and self.CM_NATIVE
        self.url = URLSpec('http://{}:{}'.format(hostname, tcpPort))

        # Attempt a connection to the server
        self.connect([self.url],
                     successCallback = self.connectSuccess,
                     failureCallback = self.connectFailure)

    def lostConnection(self):
        """ This should be overridden by a derived class to handle an
        unexpectedly lost connection to the gameserver. """
        # Handle the disconnection from the server.  This can be a reconnect,
        # simply exiting the application or anything else.
        exit()

    def connectFailure(self, statusCode, statusString):
        """ Something went wrong """
        # here we could create a reconnect task to try and connect again.
        exit()

    def connectSuccess(self):
        """ Successfully connected.  But we still can't really do
        anything until we've got the doID range. """

        # Mark interest for zone 1, 2 and 3.  There won't be anything in them,
        # it's just to display how it works for this small example.
        self.setInterestZones([1, 2, 3])

        # This method checks whether we actually have a valid doID range
        # to create distributed objects yet
        if self.haveCreateAuthority():
            # we already have one
            self.gotCreateReady()
        else:
            # Not yet, keep waiting a bit longer.
            self.accept(self.uniqueName('createReady'), self.gotCreateReady)

    def gotCreateReady(self):
        """ Ready to enter the world.  Expand our interest to include
        any other zones """

        # This method checks whether we actually have a valid doID range
        # to create distributed objects yet
        if not self.haveCreateAuthority():
            # Not ready yet.
            return

        # we are ready now, so ignore further createReady events
        self.ignore(self.uniqueName('createReady'))

        print("Client Ready")
        self.base.messenger.send("client-ready")


#================================================
#              SETUP
#================================================

#================================================
# SERVER
#================================================
def server_setup():
  # initialize the engine
  base = ShowBase(windowType='none')
  # start the server
  GameServerRepository()
  AIRepository()
  base.run()
  #pass

#================================================
# CLIENT BASE
#================================================

class ClientGame(ShowBase):
  def __init__(self):
    ShowBase.__init__(self)
    
    self.title = self.addTitle("Panda3D: Tutorial - Distributed Network (NOT CONNECTED)")
    self.inst2 = self.addInstructions(0.06, "esc: Close the client")
    self.inst2 = self.addInstructions(0.12, "See console output")

    self.accept("escape", exit)
    self.accept("client-ready", self.setConnectedMessage)
    # Start the client
    GameClientRepository(self)
  # Function to put instructions on the screen.
  def addInstructions(self, pos, msg):
    return OnscreenText(text=msg, style=1, fg=(0, 0, 0, 1), #shadow=(1, 1, 1, 1),
                        parent=base.a2dTopLeft, align=TextNode.ALeft,
                        pos=(0.08, -pos - 0.04), scale=.06)

  # Function to put title on the screen.
  def addTitle(self, text):
    return OnscreenText(text=text, style=1, pos=(-0.1, 0.09), scale=.08,
                        parent=base.a2dBottomRight, align=TextNode.ARight,
                        fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1))

  def setConnectedMessage(self):
    self.title["text"] = "Panda3D: Tutorial - Distributed Network (CONNECTED)"
    print("client connect?")

#================================================
# CLIENT
#================================================
def client_setup():
  # initialize the engine
  #base = ShowBase()
  #base.run()
  client = ClientGame()
  client.run()
  #pass
#================================================
# MAIN ENTRY POINT
#================================================
if __name__ == "__main__":
  print("[[ init network ]]")
  parser = argparse.ArgumentParser()
  parser.add_argument("-n","--network", help="server init", required=False, default=0)
  args = parser.parse_args()
  #print("args: ", args)
  #print("args.network: ", args.network)
  if args.network == '1': # 1 = server
    #print("init server")
    server_setup()
  else: # 0 = client
    #print("init client")
    client_setup()
  print("[[ network end ]]")
  #pass