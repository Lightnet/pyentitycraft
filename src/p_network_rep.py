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

def server_setup():
  pass

if __name__ == "__main__":
  print("init network")
  parser = argparse.ArgumentParser()
  #parser.add_argument("echo", help="echo the string you use here")
  #parser.add_argument("-s","--server", help="server init", default=0)
  parser.add_argument("--network", help="server init", required=False, default=0)
  args = parser.parse_args()
  #print(args.echo)
  #if args.echo:
    #print("Hello Echo")
  print("args: ", args)
  print("args.network: ", args.network)
  if args.network == '1':
    print("init server")
  else:
    print("init client")
  print("finish...")
  pass